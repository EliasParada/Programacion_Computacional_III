-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-11-2021 a las 20:28:26
-- Versión del servidor: 10.6.4-MariaDB
-- Versión de PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `fast_store`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `car_carrito`
--

CREATE TABLE `car_carrito` (
  `car_id` int(11) NOT NULL,
  `ux_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cat_categoria`
--

CREATE TABLE `cat_categoria` (
  `cat_id` int(11) NOT NULL,
  `cat_descrip` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detcar_detallecarrito`
--

CREATE TABLE `detcar_detallecarrito` (
  `detcar_id` int(11) NOT NULL,
  `car_id` int(11) DEFAULT NULL,
  `prt_id` int(11) DEFAULT NULL,
  `detcar_cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detfac_detallefactura`
--

CREATE TABLE `detfac_detallefactura` (
  `detfac_id` int(11) NOT NULL,
  `fac_id` int(11) NOT NULL,
  `prt_id` int(11) DEFAULT NULL,
  `detfac_cantidad` int(11) NOT NULL,
  `detfac_subpurchase` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `emp_empleados`
--

CREATE TABLE `emp_empleados` (
  `emp_id` int(11) NOT NULL,
  `emp_name` varchar(75) DEFAULT NULL,
  `emp_dui` varchar(12) DEFAULT NULL,
  `emp_phone` varchar(12) DEFAULT NULL,
  `emp_mail` varchar(100) DEFAULT NULL,
  `emp_address` varchar(100) DEFAULT NULL,
  `emp_DBirth` date DEFAULT NULL,
  `emp_photo` varchar(100) DEFAULT NULL,
  `pms_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fac_factura`
--

CREATE TABLE `fac_factura` (
  `fac_id` int(11) NOT NULL,
  `ux_id` int(11) DEFAULT NULL,
  `fac_date` date DEFAULT NULL,
  `fac_purchase` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pms_permissions`
--

CREATE TABLE `pms_permissions` (
  `pms_id` int(11) NOT NULL,
  `pms_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prov_proveedor`
--

CREATE TABLE `prov_proveedor` (
  `prov_id` int(11) NOT NULL,
  `prov_name` varchar(50) DEFAULT NULL,
  `prov_phone` varchar(12) NOT NULL,
  `prov_mail` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prt_producto`
--

CREATE TABLE `prt_producto` (
  `prt_id` int(11) NOT NULL,
  `prt_name` varchar(50) DEFAULT NULL,
  `prov_id` int(11) DEFAULT NULL,
  `prt_createdate` date DEFAULT NULL,
  `prt_expirationdate` date DEFAULT NULL,
  `cat_id` int(11) DEFAULT NULL,
  `prt_cost` float DEFAULT NULL,
  `prt_photo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ux_users`
--

CREATE TABLE `ux_users` (
  `ux_id` int(11) NOT NULL,
  `ux_dui` varchar(12) NOT NULL,
  `ux_name` varchar(100) DEFAULT NULL,
  `ux_tag` varchar(50) DEFAULT NULL,
  `ux_phone` varchar(12) DEFAULT NULL,
  `ux_mail` varchar(100) DEFAULT NULL,
  `ux_pass` varchar(12) DEFAULT NULL,
  `ux_DBirth` date DEFAULT NULL,
  `ux_urlphoto` varchar(100) DEFAULT NULL,
  `pms_ux` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `car_carrito`
--
ALTER TABLE `car_carrito`
  ADD PRIMARY KEY (`car_id`),
  ADD KEY `ux_id` (`ux_id`);

--
-- Indices de la tabla `cat_categoria`
--
ALTER TABLE `cat_categoria`
  ADD PRIMARY KEY (`cat_id`);

--
-- Indices de la tabla `detcar_detallecarrito`
--
ALTER TABLE `detcar_detallecarrito`
  ADD PRIMARY KEY (`detcar_id`),
  ADD KEY `car_id` (`car_id`),
  ADD KEY `prt_id` (`prt_id`);

--
-- Indices de la tabla `detfac_detallefactura`
--
ALTER TABLE `detfac_detallefactura`
  ADD PRIMARY KEY (`detfac_id`),
  ADD KEY `prt_id` (`prt_id`),
  ADD KEY `fac_id` (`fac_id`);

--
-- Indices de la tabla `emp_empleados`
--
ALTER TABLE `emp_empleados`
  ADD PRIMARY KEY (`emp_id`),
  ADD KEY `pms_id` (`pms_id`);

--
-- Indices de la tabla `fac_factura`
--
ALTER TABLE `fac_factura`
  ADD PRIMARY KEY (`fac_id`),
  ADD KEY `ux_id` (`ux_id`);

--
-- Indices de la tabla `pms_permissions`
--
ALTER TABLE `pms_permissions`
  ADD PRIMARY KEY (`pms_id`);

--
-- Indices de la tabla `prov_proveedor`
--
ALTER TABLE `prov_proveedor`
  ADD PRIMARY KEY (`prov_id`);

--
-- Indices de la tabla `prt_producto`
--
ALTER TABLE `prt_producto`
  ADD PRIMARY KEY (`prt_id`),
  ADD KEY `prov_id` (`prov_id`),
  ADD KEY `cat_id` (`cat_id`);

--
-- Indices de la tabla `ux_users`
--
ALTER TABLE `ux_users`
  ADD PRIMARY KEY (`ux_id`),
  ADD UNIQUE KEY `ux_dui` (`ux_dui`),
  ADD KEY `pms_ux` (`pms_ux`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `car_carrito`
--
ALTER TABLE `car_carrito`
  MODIFY `car_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cat_categoria`
--
ALTER TABLE `cat_categoria`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detcar_detallecarrito`
--
ALTER TABLE `detcar_detallecarrito`
  MODIFY `detcar_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detfac_detallefactura`
--
ALTER TABLE `detfac_detallefactura`
  MODIFY `detfac_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `emp_empleados`
--
ALTER TABLE `emp_empleados`
  MODIFY `emp_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `fac_factura`
--
ALTER TABLE `fac_factura`
  MODIFY `fac_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pms_permissions`
--
ALTER TABLE `pms_permissions`
  MODIFY `pms_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `prov_proveedor`
--
ALTER TABLE `prov_proveedor`
  MODIFY `prov_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `prt_producto`
--
ALTER TABLE `prt_producto`
  MODIFY `prt_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ux_users`
--
ALTER TABLE `ux_users`
  MODIFY `ux_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `car_carrito`
--
ALTER TABLE `car_carrito`
  ADD CONSTRAINT `car_carrito_ibfk_1` FOREIGN KEY (`ux_id`) REFERENCES `ux_users` (`ux_id`);

--
-- Filtros para la tabla `detcar_detallecarrito`
--
ALTER TABLE `detcar_detallecarrito`
  ADD CONSTRAINT `detcar_detallecarrito_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `car_carrito` (`car_id`),
  ADD CONSTRAINT `detcar_detallecarrito_ibfk_2` FOREIGN KEY (`prt_id`) REFERENCES `prt_producto` (`prt_id`);

--
-- Filtros para la tabla `detfac_detallefactura`
--
ALTER TABLE `detfac_detallefactura`
  ADD CONSTRAINT `detfac_detallefactura_ibfk_1` FOREIGN KEY (`prt_id`) REFERENCES `prt_producto` (`prt_id`),
  ADD CONSTRAINT `detfac_detallefactura_ibfk_2` FOREIGN KEY (`fac_id`) REFERENCES `fac_factura` (`fac_id`);

--
-- Filtros para la tabla `emp_empleados`
--
ALTER TABLE `emp_empleados`
  ADD CONSTRAINT `emp_empleados_ibfk_1` FOREIGN KEY (`pms_id`) REFERENCES `pms_permissions` (`pms_id`);

--
-- Filtros para la tabla `fac_factura`
--
ALTER TABLE `fac_factura`
  ADD CONSTRAINT `fac_factura_ibfk_1` FOREIGN KEY (`ux_id`) REFERENCES `ux_users` (`ux_id`);

--
-- Filtros para la tabla `prt_producto`
--
ALTER TABLE `prt_producto`
  ADD CONSTRAINT `prt_producto_ibfk_1` FOREIGN KEY (`prov_id`) REFERENCES `prov_proveedor` (`prov_id`),
  ADD CONSTRAINT `prt_producto_ibfk_2` FOREIGN KEY (`cat_id`) REFERENCES `cat_categoria` (`cat_id`);

--
-- Filtros para la tabla `ux_users`
--
ALTER TABLE `ux_users`
  ADD CONSTRAINT `ux_users_ibfk_1` FOREIGN KEY (`pms_ux`) REFERENCES `pms_permissions` (`pms_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
