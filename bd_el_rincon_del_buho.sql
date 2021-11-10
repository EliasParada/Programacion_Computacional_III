-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-11-2021 a las 21:43:45
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
-- Base de datos: `bd_el_rincon_del_buho`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bx_biblioteca`
--

CREATE TABLE `bx_biblioteca` (
  `bxCod` varchar(50) NOT NULL,
  `bxMuni` varchar(50) NOT NULL,
  `bxDepart` varchar(50) NOT NULL,
  `bxAddress` varchar(100) NOT NULL,
  `bxPhone` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `bx_biblioteca`
--

INSERT INTO `bx_biblioteca` (`bxCod`, `bxMuni`, `bxDepart`, `bxAddress`, `bxPhone`) VALUES
('b0001', 'usulutan', 'usulutan', '3 Calle Pte', '26232332'),
('b0002', 'San miguel', 'San miguel', '23 av sur', '99880011');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dex_indice`
--

CREATE TABLE `dex_indice` (
  `dexCod` varchar(50) NOT NULL,
  `lxCod` varchar(50) NOT NULL,
  `bxCod` varchar(50) NOT NULL,
  `dexExistence` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `dex_indice`
--

INSERT INTO `dex_indice` (`dexCod`, `lxCod`, `bxCod`, `dexExistence`) VALUES
('dex0001', 'l0001', 'b0001', 4),
('dex0002', 'l0001', 'b0002', 10),
('dex0003', 'l0002', 'b0002', 20);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `indises`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `indises` (
`dexCod` varchar(50)
,`lxTitle` varchar(50)
,`bxDepart` varchar(50)
,`bxMuni` varchar(50)
,`dexExistence` int(11)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lx_libros`
--

CREATE TABLE `lx_libros` (
  `lxCod` varchar(10) NOT NULL,
  `lxTitle` varchar(50) NOT NULL,
  `lxEdition` varchar(50) NOT NULL,
  `lxSynopsis` varchar(500) NOT NULL,
  `lxGender` varchar(20) NOT NULL,
  `lxLanguage` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `lx_libros`
--

INSERT INTO `lx_libros` (`lxCod`, `lxTitle`, `lxEdition`, `lxSynopsis`, `lxGender`, `lxLanguage`) VALUES
('l0001', 'La odisea', 'enero 2001', 'Un bato que camina mucho creo', 'Romantico', 'Castellano'),
('l0002', 'El viejo y el amr', '2019', 'un viejo que anda en el mar', 'Drama', 'Castellano');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `reservas`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `reservas` (
`rxCod` varchar(20)
,`rxDate` date
,`uxDui` varchar(20)
,`uxFullName` varchar(75)
,`dexCod` varchar(20)
,`lxCod` varchar(50)
,`lxTitle` varchar(50)
,`bxCod` varchar(50)
,`bxDepart` varchar(50)
,`bxMuni` varchar(50)
,`rxReturn` date
,`dias` int(7)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rx_reservas`
--

CREATE TABLE `rx_reservas` (
  `rxCod` varchar(20) NOT NULL,
  `rxDate` date NOT NULL,
  `uxDui` varchar(20) NOT NULL,
  `dexCod` varchar(20) NOT NULL,
  `rxReturn` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `rx_reservas`
--

INSERT INTO `rx_reservas` (`rxCod`, `rxDate`, `uxDui`, `dexCod`, `rxReturn`) VALUES
('r0001', '2021-11-09', '23232323', 'dex0002', '2021-11-23'),
('r0002', '2021-11-09', '09987666', 'dex0003', '2021-11-10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ux_usuarios`
--

CREATE TABLE `ux_usuarios` (
  `uxDUI` varchar(50) NOT NULL,
  `uxEmail` varchar(50) NOT NULL,
  `uxFullName` varchar(75) NOT NULL,
  `uxPass` varchar(50) NOT NULL,
  `uxDBirth` date NOT NULL,
  `uxAddress` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `ux_usuarios`
--

INSERT INTO `ux_usuarios` (`uxDUI`, `uxEmail`, `uxFullName`, `uxPass`, `uxDBirth`, `uxAddress`) VALUES
('09987666', 'carlos@ugb.edu.sb', 'daniel mejia', 'daniel1234', '2001-10-11', 'Usulutan'),
('23232323', 'elias@ugb.edu.sb', 'Elias Parada', 'elias1234', '2001-11-15', 'Usulutan'),
('89887777', 'william@ugb.edu.sv', 'William Amaya Garcia', 'william1234', '2001-09-22', 'Santa maria'),
('98765432', 'daniel@ugb.edu.sv', 'carlos martinez', 'carlos1234', '2001-01-22', 'Usulutan');

-- --------------------------------------------------------

--
-- Estructura para la vista `indises`
--
DROP TABLE IF EXISTS `indises`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `indises`  AS SELECT `dex_indice`.`dexCod` AS `dexCod`, `lx_libros`.`lxTitle` AS `lxTitle`, `bx_biblioteca`.`bxDepart` AS `bxDepart`, `bx_biblioteca`.`bxMuni` AS `bxMuni`, `dex_indice`.`dexExistence` AS `dexExistence` FROM ((`dex_indice` join `lx_libros` on(`dex_indice`.`lxCod` = `lx_libros`.`lxCod`)) join `bx_biblioteca` on(`dex_indice`.`bxCod` = `bx_biblioteca`.`bxCod`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `reservas`
--
DROP TABLE IF EXISTS `reservas`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `reservas`  AS SELECT `rx_reservas`.`rxCod` AS `rxCod`, `rx_reservas`.`rxDate` AS `rxDate`, `rx_reservas`.`uxDui` AS `uxDui`, `ux_usuarios`.`uxFullName` AS `uxFullName`, `rx_reservas`.`dexCod` AS `dexCod`, `dex_indice`.`lxCod` AS `lxCod`, `lx_libros`.`lxTitle` AS `lxTitle`, `dex_indice`.`bxCod` AS `bxCod`, `bx_biblioteca`.`bxDepart` AS `bxDepart`, `bx_biblioteca`.`bxMuni` AS `bxMuni`, `rx_reservas`.`rxReturn` AS `rxReturn`, to_days(`rx_reservas`.`rxReturn`) - to_days(`rx_reservas`.`rxDate`) AS `dias` FROM ((((`rx_reservas` join `ux_usuarios` on(`rx_reservas`.`uxDui` = `ux_usuarios`.`uxDUI`)) join `dex_indice` on(`rx_reservas`.`dexCod` = `dex_indice`.`dexCod`)) join `lx_libros` on(`dex_indice`.`lxCod` = `lx_libros`.`lxCod`)) join `bx_biblioteca` on(`bx_biblioteca`.`bxCod` = `dex_indice`.`bxCod`)) ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bx_biblioteca`
--
ALTER TABLE `bx_biblioteca`
  ADD PRIMARY KEY (`bxCod`);

--
-- Indices de la tabla `dex_indice`
--
ALTER TABLE `dex_indice`
  ADD PRIMARY KEY (`dexCod`),
  ADD KEY `relacion1` (`lxCod`),
  ADD KEY `relacion2` (`bxCod`);

--
-- Indices de la tabla `lx_libros`
--
ALTER TABLE `lx_libros`
  ADD PRIMARY KEY (`lxCod`);

--
-- Indices de la tabla `rx_reservas`
--
ALTER TABLE `rx_reservas`
  ADD PRIMARY KEY (`rxCod`),
  ADD KEY `relacion3` (`uxDui`),
  ADD KEY `relacion4` (`dexCod`);

--
-- Indices de la tabla `ux_usuarios`
--
ALTER TABLE `ux_usuarios`
  ADD PRIMARY KEY (`uxDUI`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `dex_indice`
--
ALTER TABLE `dex_indice`
  ADD CONSTRAINT `relacion1` FOREIGN KEY (`lxCod`) REFERENCES `lx_libros` (`lxCod`),
  ADD CONSTRAINT `relacion2` FOREIGN KEY (`bxCod`) REFERENCES `bx_biblioteca` (`bxCod`);

--
-- Filtros para la tabla `rx_reservas`
--
ALTER TABLE `rx_reservas`
  ADD CONSTRAINT `relacion3` FOREIGN KEY (`uxDui`) REFERENCES `ux_usuarios` (`uxDUI`),
  ADD CONSTRAINT `relacion4` FOREIGN KEY (`dexCod`) REFERENCES `dex_indice` (`dexCod`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
