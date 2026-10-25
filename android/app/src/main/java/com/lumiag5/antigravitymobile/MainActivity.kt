// Copyright (c) 2026 Dev LumiaG5. All rights reserved.
// Licensed under the MIT License.

package com.lumiag5.antigravitymobile

import android.Manifest
import android.annotation.SuppressLint
import android.content.ClipboardManager
import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Color
import android.net.http.SslError
import android.os.Build
import android.os.Bundle
import android.view.View
import android.webkit.*
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.WindowCompat
import com.lumiag5.antigravitymobile.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var prefs: SharedPreferences
    private val PREFS_NAME = "antigravity_prefs"
    private val KEY_SERVER_URL = "server_url"
    private val NOTIFICATION_PERMISSION_CODE = 1001

    private var hasError = false
    private var currentAttemptUrl = ""

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Configuração de tela inteira e OLED True Black
        WindowCompat.setDecorFitsSystemWindows(window, true)
        window.statusBarColor = Color.BLACK
        window.navigationBarColor = Color.BLACK

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

        setupWebView()
        setupListeners()
        requestNotificationPermission()

        val savedUrl = prefs.getString(KEY_SERVER_URL, null)
        if (savedUrl.isNullOrBlank()) {
            showConnectScreen()
        } else {
            loadServerUrl(savedUrl)
        }

        // Gerenciamento do botão Voltar do Android
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                val hasSaved = !prefs.getString(KEY_SERVER_URL, "").isNullOrBlank()
                if (binding.connectView.visibility == View.VISIBLE && hasSaved) {
                    binding.connectView.visibility = View.GONE
                    binding.swipeRefresh.visibility = View.VISIBLE
                } else if (binding.errorView.visibility == View.VISIBLE && hasSaved) {
                    showConnectScreen()
                } else if (binding.webView.canGoBack()) {
                    binding.webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val settings = binding.webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.useWideViewPort = true
        settings.loadWithOverviewMode = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.mediaPlaybackRequiresUserGesture = false
        settings.allowContentAccess = true
        settings.allowFileAccess = true
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW

        binding.webView.setBackgroundColor(Color.BLACK)

        binding.webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                if (newProgress < 100) {
                    binding.progressBar.visibility = View.VISIBLE
                    binding.progressBar.progress = newProgress
                } else {
                    binding.progressBar.visibility = View.GONE
                    binding.swipeRefresh.isRefreshing = false
                }
            }

            override fun onPermissionRequest(request: PermissionRequest?) {
                request?.grant(request.resources)
            }
        }

        binding.webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                super.onPageStarted(view, url, favicon)
                hasError = false
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                binding.progressBar.visibility = View.GONE
                binding.swipeRefresh.isRefreshing = false

                if (!hasError) {
                    binding.errorView.visibility = View.GONE
                    binding.connectView.visibility = View.GONE
                    binding.swipeRefresh.visibility = View.VISIBLE

                    val loadedUrl = currentAttemptUrl.ifBlank { url ?: "" }
                    if (loadedUrl.isNotBlank()) {
                        prefs.edit().putString(KEY_SERVER_URL, loadedUrl).apply()
                    }
                }
            }

            // Tratamento moderno de erros de rede (API 23+)
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame == true) {
                    val desc = error?.description?.toString() ?: "Falha ao conectar"
                    val code = error?.errorCode ?: 0
                    showError("Falha de Conexão", desc, code.toString(), request.url.toString())
                }
            }

            // Tratamento legado de erros (Compatibilidade com Android 7/8/9 em emuladores)
            @Suppress("DEPRECATION")
            override fun onReceivedError(
                view: WebView?,
                errorCode: Int,
                description: String?,
                failingUrl: String?
            ) {
                super.onReceivedError(view, errorCode, description, failingUrl)
                showError("Falha de Conexão", description ?: "Falha ao conectar", errorCode.toString(), failingUrl ?: "")
            }

            // Tratamento de respostas de erro HTTP (ex: 404, 500)
            override fun onReceivedHttpError(
                view: WebView?,
                request: WebResourceRequest?,
                errorResponse: WebResourceResponse?
            ) {
                super.onReceivedHttpError(view, request, errorResponse)
                if (request?.isForMainFrame == true) {
                    val status = errorResponse?.statusCode ?: 0
                    if (status >= 400) {
                        showError("Erro do Servidor", "Código de resposta HTTP $status", status.toString(), request.url.toString())
                    }
                }
            }

            // Permite certificados HTTPS válidos de túneis ou desenvolvimento local
            @SuppressLint("WebViewClientOnReceivedSslError")
            override fun onReceivedSslError(
                view: WebView?,
                handler: SslErrorHandler?,
                error: SslError?
            ) {
                handler?.proceed()
            }
        }
    }

    private fun setupListeners() {
        binding.swipeRefresh.setColorSchemeColors(Color.parseColor("#3B82F6"))
        binding.swipeRefresh.setProgressBackgroundColorSchemeColor(Color.parseColor("#161720"))
        binding.swipeRefresh.setOnRefreshListener {
            binding.webView.reload()
        }

        binding.btnRetry.setOnClickListener {
            binding.errorView.visibility = View.GONE
            val target = currentAttemptUrl.ifBlank { prefs.getString(KEY_SERVER_URL, null) }
            if (!target.isNullOrBlank()) {
                loadServerUrl(target)
            } else {
                showConnectScreen()
            }
        }

        binding.btnChangeServer.setOnClickListener {
            showConnectScreen()
        }

        // Botão Colar da Área de Transferência
        binding.btnPasteClipboard.setOnClickListener {
            val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            val clip = clipboard.primaryClip
            if (clip != null && clip.itemCount > 0) {
                val text = clip.getItemAt(0).text?.toString()?.trim() ?: ""
                if (text.isNotBlank()) {
                    binding.editServerUrlInput.setText(text)
                    binding.editServerUrlInput.setSelection(text.length)
                    Toast.makeText(this, "Link colado!", Toast.LENGTH_SHORT).show()
                }
            } else {
                Toast.makeText(this, "Área de transferência vazia.", Toast.LENGTH_SHORT).show()
            }
        }

        // Atalhos rápidos
        binding.btnPresetEmulator.setOnClickListener {
            binding.editServerUrlInput.setText("http://10.0.2.2:8765")
            binding.editServerUrlInput.setSelection(binding.editServerUrlInput.text.length)
        }

        binding.btnPresetWifi.setOnClickListener {
            binding.editServerUrlInput.setText("http://192.168.0.6:8765")
            binding.editServerUrlInput.setSelection(binding.editServerUrlInput.text.length)
        }

        binding.btnPresetCloudflare.setOnClickListener {
            val curr = binding.editServerUrlInput.text.toString().trim()
            if (!curr.startsWith("https://")) {
                binding.editServerUrlInput.setText("https://")
                binding.editServerUrlInput.setSelection(binding.editServerUrlInput.text.length)
            }
        }

        // Botão Conectar
        binding.btnConnectServer.setOnClickListener {
            val entered = binding.editServerUrlInput.text.toString().trim()
            if (entered.isNotBlank()) {
                loadServerUrl(entered)
                Toast.makeText(this, "Conectando ao servidor...", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Por favor, digite a URL do servidor.", Toast.LENGTH_SHORT).show()
            }
        }

        // Toque longo na tela abre a tela de troca de servidor
        binding.webView.setOnLongClickListener {
            showConnectScreen()
            true
        }
    }

    private fun showConnectScreen() {
        val current = prefs.getString(KEY_SERVER_URL, "") ?: ""
        binding.editServerUrlInput.setText(current)
        binding.swipeRefresh.visibility = View.GONE
        binding.errorView.visibility = View.GONE
        binding.connectView.visibility = View.VISIBLE
    }

    private fun showError(title: String, desc: String, code: String, failingUrl: String) {
        hasError = true
        runOnUiThread {
            binding.progressBar.visibility = View.GONE
            binding.swipeRefresh.isRefreshing = false
            binding.swipeRefresh.visibility = View.GONE
            binding.connectView.visibility = View.GONE
            binding.errorView.visibility = View.VISIBLE

            binding.txtErrorTitle.text = title
            binding.txtErrorDesc.text = getString(R.string.connection_error_msg)

            val details = StringBuilder()
            if (failingUrl.isNotBlank()) {
                details.append("URL: ").append(failingUrl).append("\n")
            }
            if (desc.isNotBlank()) {
                details.append("Motivo: ").append(desc)
            }
            if (code.isNotBlank()) {
                details.append(" (").append(code).append(")")
            }
            binding.txtErrorDetail.text = details.toString()
            binding.txtErrorDetail.visibility = if (details.isNotEmpty()) View.VISIBLE else View.GONE
        }
    }

    /**
     * Dedução inteligente de protocolo:
     * - Preserva scheme existente (http:// ou https://).
     * - Se for rede local (IP, localhost ou porta 8765), usa http:// (evita erro 'Invalid HTTP request received').
     * - Se não tiver porta em IP local, anexa :8765 automaticamente.
     * - Se for domínio público (Cloudflare .trycloudflare.com), usa https://.
     */
    private fun cleanServerUrl(rawUrl: String): String {
        var url = rawUrl.trim()
        if (url.isEmpty()) return ""

        while (url.endsWith("/")) {
            url = url.substring(0, url.length - 1)
        }

        val hasScheme = url.startsWith("http://", ignoreCase = true) || url.startsWith("https://", ignoreCase = true)
        val target = if (hasScheme) url.substringAfter("://") else url

        val isLocal = target.startsWith("192.168.", ignoreCase = true) ||
                      target.startsWith("10.", ignoreCase = true) ||
                      target.startsWith("172.", ignoreCase = true) ||
                      target.startsWith("127.0.0.1", ignoreCase = true) ||
                      target.startsWith("localhost", ignoreCase = true) ||
                      target.contains(":8765")

        var finalTarget = target
        if (isLocal && !finalTarget.contains(":")) {
            finalTarget = "$finalTarget:8765"
        }

        return if (hasScheme) {
            val scheme = url.substringBefore("://")
            "$scheme://$finalTarget"
        } else if (isLocal) {
            "http://$finalTarget"
        } else {
            "https://$finalTarget"
        }
    }

    private fun loadServerUrl(url: String) {
        val cleanUrl = cleanServerUrl(url)
        currentAttemptUrl = cleanUrl
        hasError = false

        binding.connectView.visibility = View.GONE
        binding.errorView.visibility = View.GONE
        binding.swipeRefresh.visibility = View.VISIBLE
        binding.progressBar.visibility = View.VISIBLE

        binding.webView.loadUrl(cleanUrl)
    }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    NOTIFICATION_PERMISSION_CODE
                )
            }
        }
    }
}
