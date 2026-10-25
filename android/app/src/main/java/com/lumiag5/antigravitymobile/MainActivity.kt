// Copyright (c) 2026 Dev LumiaG5. All rights reserved.
// Licensed under the MIT License.

package com.lumiag5.antigravitymobile

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.EditText
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AlertDialog
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

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Configuração de tela inteira OLED True Black (#000000)
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
            showServerUrlDialog(isFirstRun = true)
        } else {
            loadServerUrl(savedUrl)
        }

        // Controle do botão Voltar do Android
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (binding.webView.canGoBack()) {
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
                // Concede permissões para notificações push e áudio web
                request?.grant(request.resources)
            }
        }

        binding.webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                binding.errorView.visibility = View.GONE
                binding.swipeRefresh.isRefreshing = false
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame == true) {
                    binding.errorView.visibility = View.VISIBLE
                    binding.swipeRefresh.isRefreshing = false
                }
            }
        }
    }

    private fun setupListeners() {
        // Puxe para recarregar
        binding.swipeRefresh.setColorSchemeColors(Color.parseColor("#3B82F6"))
        binding.swipeRefresh.setProgressBackgroundColorSchemeColor(Color.parseColor("#161720"))
        binding.swipeRefresh.setOnRefreshListener {
            binding.webView.reload()
        }

        // Botão Tentar Novamente na tela de erro
        binding.btnRetry.setOnClickListener {
            binding.errorView.visibility = View.GONE
            binding.webView.reload()
        }

        // Botão Trocar Servidor
        binding.btnChangeServer.setOnClickListener {
            showServerUrlDialog(isFirstRun = false)
        }

        // Toque longo com 2 dedos para abrir configuração de servidor
        binding.webView.setOnLongClickListener {
            showServerUrlDialog(isFirstRun = false)
            true
        }
    }

    private fun loadServerUrl(url: String) {
        var cleanUrl = url.trim()
        if (!cleanUrl.startsWith("http://") && !cleanUrl.startsWith("https://")) {
            cleanUrl = "https://$cleanUrl"
        }
        binding.errorView.visibility = View.GONE
        binding.webView.loadUrl(cleanUrl)
    }

    private fun showServerUrlDialog(isFirstRun: Boolean) {
        val currentUrl = prefs.getString(KEY_SERVER_URL, "") ?: ""
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_server_url, null)
        val editUrl = dialogView.findViewById<EditText>(R.id.editServerUrl)
        editUrl.setText(currentUrl)
        if (currentUrl.isEmpty()) {
            editUrl.setHint("http://192.168.0.6:8765")
        }

        val builder = AlertDialog.Builder(this)
            .setTitle(getString(R.string.app_name))
            .setView(dialogView)
            .setPositiveButton(getString(R.string.connect)) { _, _ ->
                val enteredUrl = editUrl.text.toString().trim()
                if (enteredUrl.isNotBlank()) {
                    prefs.edit().putString(KEY_SERVER_URL, enteredUrl).apply()
                    loadServerUrl(enteredUrl)
                    Toast.makeText(this, "Servidor salvo com sucesso!", Toast.LENGTH_SHORT).show()
                } else if (isFirstRun) {
                    // Fallback para IP local padrão
                    val defaultUrl = "http://192.168.0.6:8765"
                    prefs.edit().putString(KEY_SERVER_URL, defaultUrl).apply()
                    loadServerUrl(defaultUrl)
                }
            }

        if (!isFirstRun) {
            builder.setNegativeButton(getString(R.string.cancel), null)
        }

        builder.setCancelable(!isFirstRun)
        builder.show()
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
