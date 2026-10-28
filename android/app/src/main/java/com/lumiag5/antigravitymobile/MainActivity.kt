// Copyright (c) 2026 Dev LumiaG5. All rights reserved.
// Licensed under the MIT License.

package com.lumiag5.antigravitymobile

import android.Manifest
import android.annotation.SuppressLint
import android.content.BroadcastReceiver
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.net.http.SslError
import android.os.BatteryManager
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.Settings
import android.view.View
import android.view.WindowManager
import android.webkit.*
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.journeyapps.barcodescanner.ScanContract
import com.journeyapps.barcodescanner.ScanIntentResult
import com.journeyapps.barcodescanner.ScanOptions
import com.lumiag5.antigravitymobile.databinding.ActivityMainBinding
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var prefs: SharedPreferences
    private val PREFS_NAME = "antigravity_prefs"
    private val KEY_SERVER_URL = "server_url"
    private val NOTIFICATION_PERMISSION_CODE = 1001
    private val CAMERA_PERMISSION_CODE = 1002

    private var hasError = false
    private var currentAttemptUrl = ""

    private var isBatteryReceiverRegistered = false
    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == Intent.ACTION_BATTERY_CHANGED) {
                val level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                val scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                val status = intent.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
                val isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING ||
                        status == BatteryManager.BATTERY_STATUS_FULL
                if (level >= 0 && scale > 0) {
                    val pct = (level * 100 / scale.toFloat()).toInt()
                    binding.webView.evaluateJavascript(
                        "if (window.BatteryManager && window.BatteryManager.update) window.BatteryManager.update($pct, $isCharging);",
                        null
                    )
                }
            }
        }
    }

    // Lançador do Scanner de QR Code nativo (ZXing)
    private val qrScanLauncher = registerForActivityResult(ScanContract()) { result: ScanIntentResult ->
        if (result.contents != null) {
            val scanned = result.contents.trim()
            if (scanned.isNotBlank()) {
                handleScannedUrl(scanned)
            }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Configuração de tela inteira imersiva (oculta HUD/status bar) e OLED True Black
        window.statusBarColor = Color.BLACK
        window.navigationBarColor = Color.BLACK
        applyFullScreenImmersive()

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

        setupWebView()
        setupListeners()
        requestNotificationPermission()
        registerBatteryReceiver()

        // Exigência: Ao fechar e reabrir o app, sempre inicia deslogado na tela de gerenciamento de sessão
        showConnectScreen()

        // Gerenciamento do botão Voltar do Android
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (binding.connectView.visibility == View.VISIBLE) {
                    // Já na tela de sessão: encerra o app
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                } else if (binding.errorView.visibility == View.VISIBLE) {
                    showConnectScreen()
                } else {
                    // No dashboard: voltar desloga para a tela de sessão
                    showConnectScreen()
                }
            }
        })
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus) {
            applyFullScreenImmersive()
        }
    }

    private fun applyFullScreenImmersive() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            window.attributes.layoutInDisplayCutoutMode =
                WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            WindowCompat.setDecorFitsSystemWindows(window, false)
            val controller = WindowCompat.getInsetsController(window, window.decorView)
            controller.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            controller.hide(WindowInsetsCompat.Type.statusBars())
        } else {
            @Suppress("DEPRECATION")
            WindowCompat.setDecorFitsSystemWindows(window, false)
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility = (
                View.SYSTEM_UI_FLAG_FULLSCREEN
                or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            )
        }
    }

    private fun registerBatteryReceiver() {
        if (!isBatteryReceiverRegistered) {
            try {
                registerReceiver(batteryReceiver, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
                isBatteryReceiverRegistered = true
            } catch (e: Exception) {}
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (isBatteryReceiverRegistered) {
            try {
                unregisterReceiver(batteryReceiver)
                isBatteryReceiverRegistered = false
            } catch (e: Exception) {}
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val settings = binding.webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.useWideViewPort = true
        settings.loadWithOverviewMode = true
        settings.cacheMode = WebSettings.LOAD_NO_CACHE
        settings.mediaPlaybackRequiresUserGesture = false
        settings.allowContentAccess = true
        settings.allowFileAccess = true
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW

        binding.webView.setBackgroundColor(Color.BLACK)

        binding.webView.isVerticalScrollBarEnabled = true
        binding.webView.overScrollMode = View.OVER_SCROLL_IF_CONTENT_SCROLLS

        // Interface Javascript para comunicação bidirecional com a web
        binding.webView.addJavascriptInterface(AndroidBridge(), "AndroidBridge")

        binding.webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                if (newProgress < 100) {
                    binding.progressBar.visibility = View.VISIBLE
                    binding.progressBar.progress = newProgress
                } else {
                    binding.progressBar.visibility = View.GONE
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

                if (!hasError) {
                    binding.errorView.visibility = View.GONE
                    binding.connectView.visibility = View.GONE
                    binding.webView.visibility = View.VISIBLE

                    val loadedUrl = currentAttemptUrl.ifBlank { url ?: "" }
                    if (loadedUrl.isNotBlank()) {
                        // Persiste o endereço base do servidor (removendo parâmetros temporários)
                        val baseUrl = cleanServerUrl(loadedUrl).substringBefore("?")
                        prefs.edit().putString(KEY_SERVER_URL, baseUrl).apply()
                    }

                    // Notifica a página web sobre a versão nativa do APK e inicializa o menu de update e bateria
                    val currentBattery = AndroidBridge().getBatteryLevel()
                    val currentCharging = AndroidBridge().isBatteryCharging()
                    binding.webView.evaluateJavascript(
                        "if (typeof updateAppVersionBadge === 'function') updateAppVersionBadge(); if (window.ApkUpdateManager) ApkUpdateManager.init(); if (window.BatteryManager && window.BatteryManager.update) window.BatteryManager.update($currentBattery, $currentCharging);",
                        null
                    )
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

            // Tratamento legado de erros (Compatibilidade com emuladores)
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

        // Opção 1: Voltar à Sessão Ativa (Reconecta sem pedir novo PIN)
        binding.btnResumeSession.setOnClickListener {
            val saved = prefs.getString(KEY_SERVER_URL, null)
            if (!saved.isNullOrBlank()) {
                Toast.makeText(this, "Retomando sessão ativa...", Toast.LENGTH_SHORT).show()
                loadServerUrl(saved)
            } else {
                showConnectScreen()
            }
        }

        // Opção 2: Entrar com QR Code (abre a câmera para ler o QR Code do terminal do PC)
        binding.btnScanQr.setOnClickListener {
            startQrScanner()
        }

        // Opção 3: Nova Sessão (Limpa token anterior e abre formulário de conexão)
        binding.btnNewSession.setOnClickListener {
            startNewSession()
        }

        // Botão de Colar URL
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

        // Botão Conectar do formulário manual
        binding.btnConnectServer.setOnClickListener {
            val entered = binding.editServerUrlInput.text.toString().trim()
            if (entered.isNotBlank()) {
                loadServerUrl(entered)
                Toast.makeText(this, "Conectando ao servidor...", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Por favor, digite a URL do servidor.", Toast.LENGTH_SHORT).show()
            }
        }

        // Toque longo na tela abre a tela de sessão
        binding.webView.setOnLongClickListener {
            showConnectScreen()
            true
        }
    }

    private fun startQrScanner() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.CAMERA),
                CAMERA_PERMISSION_CODE
            )
        } else {
            launchScanner()
        }
    }

    private fun launchScanner() {
        try {
            val options = ScanOptions().apply {
                setDesiredBarcodeFormats(ScanOptions.QR_CODE)
                setPrompt("Aponte para o QR Code no terminal do PC")
                setCameraId(0)
                setBeepEnabled(true)
                setBarcodeImageEnabled(false)
                setOrientationLocked(true)
            }
            qrScanLauncher.launch(options)
        } catch (e: Exception) {
            Toast.makeText(this, "Erro ao abrir câmera: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    private fun handleScannedUrl(scanned: String) {
        val cleanUrl = cleanServerUrl(scanned)
        binding.editServerUrlInput.setText(cleanUrl)
        Toast.makeText(this, "QR Code lido com sucesso!", Toast.LENGTH_SHORT).show()
        loadServerUrl(cleanUrl)
    }

    private fun startNewSession() {
        // Remove token de autenticação anterior no WebView para forçar novo PIN
        binding.webView.evaluateJavascript(
            "try { localStorage.removeItem('antigravity_auth_token'); localStorage.removeItem('antigravity_auth_expiry'); } catch(e) {}",
            null
        )
        binding.layoutManualInput.visibility = View.VISIBLE
        val current = prefs.getString(KEY_SERVER_URL, "") ?: ""
        if (current.isNotBlank() && binding.editServerUrlInput.text.isNullOrBlank()) {
            binding.editServerUrlInput.setText(current)
        }
        binding.editServerUrlInput.requestFocus()
        Toast.makeText(this, "Iniciando nova sessão. Digite o PIN quando solicitado.", Toast.LENGTH_SHORT).show()
    }

    private fun showConnectScreen() {
        val saved = prefs.getString(KEY_SERVER_URL, null)

        binding.webView.visibility = View.GONE
        binding.errorView.visibility = View.GONE
        binding.connectView.visibility = View.VISIBLE

        if (!saved.isNullOrBlank()) {
            binding.boxResumeSession.visibility = View.VISIBLE
            binding.txtSavedServerUrl.text = saved
            binding.layoutManualInput.visibility = View.GONE
            binding.editServerUrlInput.setText(saved)
        } else {
            binding.boxResumeSession.visibility = View.GONE
            binding.layoutManualInput.visibility = View.VISIBLE
        }
    }

    private fun showError(title: String, desc: String, code: String, failingUrl: String) {
        hasError = true
        runOnUiThread {
            binding.progressBar.visibility = View.GONE
            binding.webView.visibility = View.GONE
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
     * - Preserva scheme existente (http:// ou https://) e query parameters (?pin=...).
     * - Se for rede local (IP, localhost ou porta 8765), usa http://.
     * - Se não tiver porta em IP local, anexa :8765 automaticamente.
     * - Se for domínio público (Cloudflare .trycloudflare.com), usa https://.
     */
    private fun cleanServerUrl(rawUrl: String): String {
        var url = rawUrl.trim()
        if (url.isEmpty()) return ""

        val hasScheme = url.startsWith("http://", ignoreCase = true) || url.startsWith("https://", ignoreCase = true)
        val scheme = if (hasScheme) url.substringBefore("://") else ""
        var rest = if (hasScheme) url.substringAfter("://") else url

        val query = if (rest.contains("?")) "?" + rest.substringAfter("?") else ""
        var hostPort = if (rest.contains("?")) rest.substringBefore("?") else rest

        while (hostPort.endsWith("/")) {
            hostPort = hostPort.substring(0, hostPort.length - 1)
        }

        val isLocal = hostPort.startsWith("192.168.", ignoreCase = true) ||
                      hostPort.startsWith("10.", ignoreCase = true) ||
                      hostPort.startsWith("172.", ignoreCase = true) ||
                      hostPort.startsWith("127.0.0.1", ignoreCase = true) ||
                      hostPort.startsWith("localhost", ignoreCase = true) ||
                      hostPort.contains(":8765")

        if (isLocal && !hostPort.contains(":")) {
            hostPort = "$hostPort:8765"
        }

        val finalScheme = if (hasScheme) {
            scheme
        } else if (isLocal) {
            "http"
        } else {
            "https"
        }

        return "$finalScheme://$hostPort$query"
    }

    private fun loadServerUrl(url: String) {
        val cleanUrl = cleanServerUrl(url)
        currentAttemptUrl = cleanUrl
        hasError = false

        binding.connectView.visibility = View.GONE
        binding.errorView.visibility = View.GONE
        binding.webView.visibility = View.VISIBLE
        binding.progressBar.visibility = View.VISIBLE

        binding.webView.loadUrl(cleanUrl)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                launchScanner()
            } else {
                Toast.makeText(this, "Permissão de câmera necessária para escanear QR Code.", Toast.LENGTH_LONG).show()
            }
        }
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

    private fun startApkDownload(downloadUrl: String, version: String) {
        Toast.makeText(this, "Iniciando download da atualização v$version...", Toast.LENGTH_SHORT).show()
        Thread {
            try {
                var currentUrl = downloadUrl
                var conn: HttpURLConnection
                var responseCode: Int

                // Segue redirecionamentos automáticos do GitHub Releases
                while (true) {
                    val urlObj = URL(currentUrl)
                    conn = urlObj.openConnection() as HttpURLConnection
                    conn.instanceFollowRedirects = true
                    conn.connectTimeout = 15000
                    conn.readTimeout = 30000
                    conn.connect()
                    responseCode = conn.responseCode
                    if (responseCode in 300..399) {
                        val loc = conn.getHeaderField("Location")
                        if (!loc.isNullOrBlank()) {
                            currentUrl = loc
                            continue
                        }
                    }
                    break
                }

                if (responseCode != HttpURLConnection.HTTP_OK) {
                    runOnUiThread {
                        Toast.makeText(this, "Falha no download (HTTP $responseCode)", Toast.LENGTH_LONG).show()
                    }
                    return@Thread
                }

                val downloadDir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS) ?: cacheDir
                val apkFile = File(downloadDir, "Antigravity-$version.apk")
                if (apkFile.exists()) apkFile.delete()

                conn.inputStream.use { input ->
                    FileOutputStream(apkFile).use { output ->
                        val buffer = ByteArray(8192)
                        var bytesRead: Int
                        while (input.read(buffer).also { bytesRead = it } != -1) {
                            output.write(buffer, 0, bytesRead)
                        }
                    }
                }

                runOnUiThread {
                    Toast.makeText(this, "Download concluído! Abrindo instalador...", Toast.LENGTH_SHORT).show()
                    installApk(apkFile)
                }
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this, "Erro ao baixar atualização: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }.start()
    }

    private fun installApk(file: File) {
        try {
            if (!file.exists()) return

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                if (!packageManager.canRequestPackageInstalls()) {
                    Toast.makeText(this, "Permita a instalação para atualizar o app", Toast.LENGTH_LONG).show()
                    val permissionIntent = Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES).apply {
                        data = Uri.parse("package:$packageName")
                    }
                    startActivity(permissionIntent)
                }
            }

            val apkUri = FileProvider.getUriForFile(
                this,
                "${packageName}.fileprovider",
                file
            )

            val installIntent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(apkUri, "application/vnd.android.package-archive")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
            }
            startActivity(installIntent)
        } catch (e: Exception) {
            Toast.makeText(this, "Erro ao abrir instalador: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    // Bridge JS chamada pelo WebView da interface web
    inner class AndroidBridge {
        @JavascriptInterface
        fun exitSession() {
            runOnUiThread {
                showConnectScreen()
            }
        }

        @JavascriptInterface
        fun isAndroidApp(): Boolean {
            return true
        }

        @JavascriptInterface
        fun getAppVersion(): String {
            return try {
                val pInfo = packageManager.getPackageInfo(packageName, 0)
                pInfo.versionName ?: "2.4.3"
            } catch (e: Exception) {
                "2.4.3"
            }
        }

        @JavascriptInterface
        fun getAppVersionCode(): Int {
            return try {
                val pInfo = packageManager.getPackageInfo(packageName, 0)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                    pInfo.longVersionCode.toInt()
                } else {
                    @Suppress("DEPRECATION")
                    pInfo.versionCode
                }
            } catch (e: Exception) {
                2421
            }
        }

        @JavascriptInterface
        fun downloadAndInstallApk(url: String, version: String) {
            runOnUiThread {
                startApkDownload(url, version)
            }
        }

        @JavascriptInterface
        fun getBatteryLevel(): Int {
            return try {
                val bm = getSystemService(Context.BATTERY_SERVICE) as? BatteryManager
                val capacity = bm?.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY) ?: -1
                if (capacity in 0..100) {
                    capacity
                } else {
                    val intent = registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
                    val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
                    val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
                    if (level >= 0 && scale > 0) {
                        (level * 100 / scale.toFloat()).toInt()
                    } else -1
                }
            } catch (e: Exception) {
                -1
            }
        }

        @JavascriptInterface
        fun isBatteryCharging(): Boolean {
            return try {
                val intent = registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
                val status = intent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
                status == BatteryManager.BATTERY_STATUS_CHARGING ||
                        status == BatteryManager.BATTERY_STATUS_FULL
            } catch (e: Exception) {
                false
            }
        }
    }
}
