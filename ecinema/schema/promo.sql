
DROP TABLE IF EXISTS `promo`;

CREATE TABLE `promo` (
  `promo_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `code` varchar(100) NOT NULL,
  `promo` double NOT NULL,
  `promo_description` varchar(1024) DEFAULT '',
  exp_date datetime NOT NULL
)
