#include "PostgresUserRepository.h"

PostgresUserRepository::PostgresUserRepository(const DbConfig& cfg)
    : connStr_(cfg.connStr) {
}

User PostgresUserRepository::mapRow(const pqxx::row& r) {
    User u;
    u.id = r["id"].as<long long>();
    u.email = r["email"].as<std::string>();
    u.login = r["login"].as<std::string>();
    u.passwordHash = r["password_hash"].as<std::string>();
    if (!r["created_at"].is_null()) u.createdAt = r["created_at"].c_str();
    return u;
}

User PostgresUserRepository::create(const User& u) {
    pqxx::connection c(connStr_);
    pqxx::work tx(c);

    auto res = tx.exec_params(
        "INSERT INTO users(email, login, password_hash) VALUES($1,$2,$3) "
        "RETURNING id, email, login, password_hash, created_at",
        u.email, u.login, u.passwordHash
    );
    tx.commit();
    return mapRow(res[0]);
}

std::optional<User> PostgresUserRepository::findByLogin(const std::string& login) {
    pqxx::connection c(connStr_);
    pqxx::work tx(c);

    auto res = tx.exec_params(
        "SELECT id, email, login, password_hash, created_at FROM users WHERE login=$1",
        login
    );
    if (res.empty()) return std::nullopt;
    return mapRow(res[0]);
}

std::optional<User> PostgresUserRepository::findByEmail(const std::string& email) {
    pqxx::connection c(connStr_);
    pqxx::work tx(c);

    auto res = tx.exec_params(
        "SELECT id, email, login, password_hash, created_at FROM users WHERE email=$1",
        email
    );
    if (res.empty()) return std::nullopt;
    return mapRow(res[0]);
}