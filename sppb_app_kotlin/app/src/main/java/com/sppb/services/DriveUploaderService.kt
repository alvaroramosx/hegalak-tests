package com.sppb.services

import android.content.Context
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.api.client.extensions.android.http.AndroidHttp
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.drive.Drive
import com.google.api.services.drive.DriveScopes
import com.google.api.services.drive.model.File
import com.google.api.client.http.FileContent
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException

/**
 * Servicio para subir archivos a Google Drive
 * Análogo a drive_uploader.py usando Google Drive API para Android
 */
class DriveUploaderService(private val context: Context) {
    
    companion object {
        private val SCOPES = listOf(DriveScopes.DRIVE_FILE, DriveScopes.DRIVE)
    }
    
    /**
     * Sube un archivo a una carpeta de Google Drive
     * 
     * @param localPath Ruta local del archivo
     * @param folderId ID de la carpeta de destino en Drive
     * @return Pair<String, String> (fileId, webViewLink)
     */
    suspend fun uploadFileToDrive(
        localPath: String,
        folderId: String
    ): Pair<String, String> = withContext(Dispatchers.IO) {
        try {
            val driveService = getDriveService() ?: throw IOException("No se pudo obtener servicio de Drive")
            
            // Verificar que la carpeta existe y es realmente una carpeta
            val folderMeta = driveService.files()
                .get(folderId)
                .setFields("id, name, mimeType")
                .execute()
            
            if (folderMeta.mimeType != "application/vnd.google-apps.folder") {
                throw IOException("El ID proporcionado no corresponde a una carpeta")
            }
            
            // Preparar metadatos del archivo
            val localFile = java.io.File(localPath)
            val fileMetadata = File()
            fileMetadata.name = localFile.name
            fileMetadata.parents = listOf(folderId)
            
            // Preparar contenido del archivo
            val mediaContent = FileContent(getMimeType(localPath), localFile)
            
            // Subir archivo
            val uploadedFile = driveService.files()
                .create(fileMetadata, mediaContent)
                .setFields("id, webViewLink")
                .execute()
            
            Pair(uploadedFile.id, uploadedFile.webViewLink ?: "")
        } catch (e: Exception) {
            throw IOException("Error al subir archivo: ${e.message}", e)
        }
    }
    
    /**
     * Obtiene el servicio de Drive usando las credenciales del usuario actual
     */
    private fun getDriveService(): Drive? {
        val account = GoogleSignIn.getLastSignedInAccount(context) ?: return null
        
        val credential = GoogleAccountCredential.usingOAuth2(
            context,
            SCOPES
        )
        credential.selectedAccount = account.account
        
        return Drive.Builder(
            AndroidHttp.newCompatibleTransport(),
            GsonFactory.getDefaultInstance(),
            credential
        )
            .setApplicationName("SPPB")
            .build()
    }
    
    /**
     * Determina el MIME type del archivo según su extensión
     */
    private fun getMimeType(filePath: String): String {
        return when {
            filePath.endsWith(".pdf") -> "application/pdf"
            filePath.endsWith(".xlsx") -> "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filePath.endsWith(".xls") -> "application/vnd.ms-excel"
            filePath.endsWith(".png") -> "image/png"
            filePath.endsWith(".jpg") || filePath.endsWith(".jpeg") -> "image/jpeg"
            else -> "application/octet-stream"
        }
    }
    
    /**
     * Extrae el ID de carpeta desde una URL de Google Drive
     */
    fun extractFolderIdFromUrl(url: String): String? {
        // Formato: https://drive.google.com/drive/folders/FOLDER_ID
        val folderRegex = Regex("/folders/([a-zA-Z0-9_-]+)")
        val match = folderRegex.find(url)
        if (match != null) {
            return match.groupValues[1]
        }
        
        // Formato alternativo: ?id=FOLDER_ID
        val idRegex = Regex("[?&]id=([a-zA-Z0-9_-]+)")
        val idMatch = idRegex.find(url)
        return idMatch?.groupValues?.get(1)
    }
    
    /**
     * Configura las opciones de inicio de sesión de Google
     */
    fun getSignInOptions(): GoogleSignInOptions {
        return GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestEmail()
            .requestScopes(
                com.google.android.gms.common.api.Scope(DriveScopes.DRIVE_FILE),
                com.google.android.gms.common.api.Scope(DriveScopes.DRIVE)
            )
            .build()
    }
}


