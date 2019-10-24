
DROP TABLE IF EXISTS `credit_card`;

CREATE TABLE `credit_card` (
  `credit_card_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `cid` int(11) NOT NULL,
  `card_number` varchar(100) NOT NULL,
  `cvv` varchar(100) NOT NULL,
  `exp_date` datetime NOT NULL,
  FOREIGN KEY (cid) REFERENCES customer (customer_id)
)
