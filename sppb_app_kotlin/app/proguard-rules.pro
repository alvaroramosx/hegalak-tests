# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Keep Jetpack Compose classes
-keep class androidx.compose.** { *; }

# Keep data classes
-keep class com.sppb.data.models.** { *; }

# Keep Google API classes
-keep class com.google.api.** { *; }
-keep class com.google.android.gms.** { *; }

# Apache POI
-dontwarn org.apache.poi.**
-dontwarn org.apache.xmlbeans.**
-keep class org.apache.poi.** { *; }

# iText
-dontwarn com.itextpdf.**
-keep class com.itextpdf.** { *; }


