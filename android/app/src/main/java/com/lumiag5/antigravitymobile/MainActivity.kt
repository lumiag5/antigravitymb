// Copyright (c) 2026 Dev LumiaG5. All rights reserved.
// Licensed under the MIT License.

package com.lumiag5.antigravitymobile

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
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

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // OLED True Black
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

        // Back press handling
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                val hasSaved = !prefs.getString(KEY_SERVER_URL, "").isNullOrBlank()
                if (binding.connectView.visibility == View.VISIBLE && hasSaved) {
                    binding.connectView.visibility = View.GONE
                    binding.swipeRefresh.visibility = View.VISIBLE
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

            override fun onReceivedSslError(
                view: WebView?,
                handler: SslErrorHandler?,
                error: SslError?
            ) {
                // Permite certificados de túneis Cloudflare ou IPs locais sem bloquear
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
            binding.webView.reload()
        }

        binding.btnChangeServer.setOnClickListener {
            showConnectScreen()
        }

        binding.btnConnectServer.setOnClickListener {
            val entered = binding.editServerUrlInput.text.toString().trim()
            if (entered.isNotBlank()) {
                prefs.edit().putString(KEY_SERVER_URL, entered).apply()
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

    private fun loadServerUrl(url: String) {
        var cleanUrl = url.trim()
        if (!cleanUrl.startsWith("http://") && !cleanUrl.startsWith("https://")) {
            cleanUrl = "https://$cleanUrl"
        }
        binding.connectView.visibility = View.GONE
        binding.errorView.visibility = View.GONE
        binding.swipeRefresh.visibility = View.VISIBLE
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
