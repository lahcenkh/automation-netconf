CREATE TABLE "routers_info" (
	"id"	INTEGER NOT NULL,
	"router_name"	TEXT,
	"router_ipaddress"	TEXT,
	"router_technology"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "interfaces" (
	"router_name"	TEXT,
	"interface_name"	TEXT,
	"description"	TEXT,
	"admin_state"	TEXT,
	"operation_state"	TEXT,
	"mac_address"	TEXT,
	"speed"	TEXT,
	"ipaddress"	TEXT,
	"mask"	TEXT
);