# Hook: on_skewness_detected

## Gatilho
Disparado sempre que o `distribution_fitter` detecta uma assimetria severa (> 1 ou < -1) em uma variável contínua.

## Ação Automática
Gera um alerta silencioso no log sugerindo a aplicação de transformação Logarítmica antes de qualquer modelo de regressão linear.