# Happy Teeth - Proyecto 2

## Archivo principal
Ejecutar:

```bash
python Inicio.py
```

La interfaz está hecha con **Tkinter**, que forma parte de Python y no requiere instalar un paquete adicional.

## Inicio de sesión temporal
El Proyecto 1 no guardaba contraseñas. Mientras se conecta SQL Server, los funcionarios que vienen del XML usan temporalmente la contraseña:

`1234`

El inicio de sesión utiliza el campo `Usuario` del funcionario. Los usuarios de prueba del XML son, por ejemplo, `Dr Ceciliano` y `Dr Simi`.

## Organización de la interfaz
- `interfaz/InterfazLogin.py`: inicio de sesión.
- `interfaz/InterfazMenu.py`: menú principal.
- `interfaz/InterfazPadres.py`: mantenimiento de padres/encargados.
- `interfaz/InterfazNinos.py`: mantenimiento y búsqueda de niños.
- `interfaz/InterfazFuncionarios.py`: mantenimiento de funcionarios.
- `interfaz/InterfazServicios.py`: mantenimiento de servicios.
- `interfaz/InterfazFacturacion.py`: registro de atención y factura.
- `interfaz/InterfazConsultaFacturas.py`: consulta y pago.
- `interfaz/Estilos.py`: colores y formato común.

## Nota
Los XML se conservan **temporalmente** para que la interfaz pueda probarse antes de terminar SQL Server. La carpeta `respaldo_consola` contiene la versión original antes de quitar los menús por consola.
