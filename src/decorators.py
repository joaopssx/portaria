"""Decoradores criados para o sistema.

Um decorador e uma funcao que recebe outra funcao e devolve uma nova funcao
"embrulhada", acrescentando comportamento sem alterar o codigo original.
"""

import functools

# Guarda o historico de operacoes registradas pelo decorador @log_operacao.
historico = []


def log_operacao(func):
    """Registra no historico toda vez que a funcao decorada e executada."""

    @functools.wraps(func)  # preserva nome e docstring da funcao original
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        historico.append(f"{func.__name__} executada")
        return resultado

    return wrapper


def contar_chamadas(func):
    """Conta quantas vezes a funcao decorada foi chamada (em func.chamadas)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.chamadas += 1
        return func(*args, **kwargs)

    wrapper.chamadas = 0
    return wrapper
