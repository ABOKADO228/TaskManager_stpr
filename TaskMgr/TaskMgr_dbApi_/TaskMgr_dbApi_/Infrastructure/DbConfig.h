#pragma once
#include <string>
#include <cstdlib>

struct DbConfig {
    std::string connStr;

    static DbConfig fromEnv() {
      
        const char* cs = std::getenv("PG_CONN");
        DbConfig c;
        c.connStr = cs ? cs : "host=localhost port=5432 dbname=taskmgr user=postgres password=postgres";
        return c;
    }
};