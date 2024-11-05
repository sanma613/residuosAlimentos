# excepciones.py


class SistemaOperativoError(Exception):
    """Error general del sistema."""

    pass


class AlimentoNoEncontradoError(Exception):
    """Se lanza cuando no se encuentra el alimento buscado."""

    pass


class UnidadesInsuficientesError(Exception):
    """Se lanza cuando la cantidad solicitada supera las unidades disponibles."""

    pass


class CarritoVacioError(Exception):
    """Se lanza cuando el carrito está vacío y se intenta finalizar una adquisición."""

    pass


class AlimentosNoSeleccionadosError(Exception):
    """Se lanza cuando no se proporciona un filtro para buscar o seleccionar alimentos."""

    pass
