package com.sppb

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.sppb.ui.screens.*
import com.sppb.ui.theme.SPPBTheme
import com.sppb.viewmodels.SppbViewModel

/**
 * Activity principal de la aplicación SPPB
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        setContent {
            SPPBTheme {
                SppbApp()
            }
        }
    }
}

/**
 * Rutas de navegación
 */
sealed class Screen(val route: String) {
    object Start : Screen("start")
    object BalanceFeet : Screen("balance_feet")
    object BalanceSemi : Screen("balance_semi")
    object BalanceTandem : Screen("balance_tandem")
    object Gait : Screen("gait")
    object Chair : Screen("chair")
    object Summary : Screen("summary")
}

/**
 * Aplicación principal con navegación
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SppbApp() {
    val navController = rememberNavController()
    val viewModel: SppbViewModel = viewModel()
    val scores = viewModel.getCurrentScores()
    
    // Calcular progreso actual
    val currentRoute = navController.currentBackStackEntry?.destination?.route
    val progress = when (currentRoute) {
        Screen.Start.route -> 0f
        Screen.BalanceFeet.route -> 0f
        Screen.BalanceSemi.route -> 0.2f
        Screen.BalanceTandem.route -> 0.4f
        Screen.Gait.route -> 0.6f
        Screen.Chair.route -> 0.8f
        Screen.Summary.route -> 1f
        else -> 0f
    }
    
    Scaffold(
        topBar = {
            if (currentRoute != Screen.Start.route) {
                TopAppBar(
                    title = {
                        Column {
                            Text(
                                text = "SPPB Test",
                                style = MaterialTheme.typography.titleMedium
                            )
                            Text(
                                text = "Equilibrio ${scores.balanceScore}/4 · Marcha ${scores.gaitScore}/4 · Silla ${scores.chairScore}/4 · Total ${scores.total}/12",
                                style = MaterialTheme.typography.bodySmall
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        titleContentColor = MaterialTheme.colorScheme.onPrimary
                    )
                )
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Barra de progreso
            if (currentRoute != Screen.Start.route) {
                LinearProgressIndicator(
                    progress = progress,
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.secondary,
                    trackColor = MaterialTheme.colorScheme.surfaceVariant
                )
            }
            
            // Navegación
            NavHost(
                navController = navController,
                startDestination = Screen.Start.route
            ) {
                composable(Screen.Start.route) {
                    StartScreen(
                        viewModel = viewModel,
                        onNext = {
                            navController.navigate(Screen.BalanceFeet.route)
                        }
                    )
                }
                
                composable(Screen.BalanceFeet.route) {
                    BalanceFeetScreen(
                        viewModel = viewModel,
                        onNext = {
                            navController.navigate(Screen.BalanceSemi.route)
                        },
                        onBack = {
                            navController.popBackStack()
                        }
                    )
                }
                
                composable(Screen.BalanceSemi.route) {
                    BalanceSemiScreen(
                        viewModel = viewModel,
                        onNext = {
                            navController.navigate(Screen.BalanceTandem.route)
                        },
                        onBack = {
                            navController.popBackStack()
                        }
                    )
                }
                
                composable(Screen.BalanceTandem.route) {
                    BalanceTandemScreen(
                        viewModel = viewModel,
                        onNext = {
                            navController.navigate(Screen.Gait.route)
                        },
                        onBack = {
                            navController.popBackStack()
                        }
                    )
                }
                
                composable(Screen.Gait.route) {
                    GaitScreen(
                        viewModel = viewModel,
                        onNext = {
                            navController.navigate(Screen.Chair.route)
                        },
                        onBack = {
                            navController.popBackStack()
                        }
                    )
                }
                
                composable(Screen.Chair.route) {
                    ChairScreen(
                        viewModel = viewModel,
                        onFinish = {
                            navController.navigate(Screen.Summary.route)
                        },
                        onBack = {
                            navController.popBackStack()
                        }
                    )
                }
                
                composable(Screen.Summary.route) {
                    SummaryScreen(
                        viewModel = viewModel,
                        onNewTest = {
                            navController.navigate(Screen.Start.route) {
                                popUpTo(Screen.Start.route) { inclusive = true }
                            }
                        }
                    )
                }
            }
        }
    }
}


