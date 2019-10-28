
DROP TABLE IF EXISTS address;

CREATE TABLE address (
  address_id INTEGER PRIMARY KEY AUTOINCREMENT,
  street varchar(100) NOT NULL,
  city varchar(100) NOT NULL,
  state varchar(100) NOT NULL,
  zip_code varchar(100) NOT NULL
)
