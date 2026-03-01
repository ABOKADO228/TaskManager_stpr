#include "PgUserRepository.h"

PgUserRepository::PgUserRepository(drogon::orm::DbClientPtr db)
    : db_(std::move(db)) {
}

bool PgUserRepository::usernameExists(const std::string& username) {
    auto r = db_->execSqlSync(
        "SELECT 1 FROM users WHERE username=$1 LIMIT 1",
        username
    );
    return !r.empty();
}

std::optional<User> PgUserRepository::findByUsername(const std::string& username) {
    auto r = db_->execSqlSync(
        "SELECT id, username, password_hash FROM users WHERE username=$1 LIMIT 1",
        username
    );
    if (r.empty()) return std::nullopt;

    User u;
    u.id =û r[0]["id"].as<std::string>();
    u.username = r[0]["username"].as<std::string>();
    u.passwordHash = r[0]["password_hash"].as<std::string>();
    return u;
}

User PgUserRepository::create(const User& user) {
    auto r = db_->execSqlSync(
        "INSERT INTO users (username, password_hash) VALUES ($1, $2) RETURNING id",
        user.username,
        user.passwordHash
    );

    User created = user;
    if (!r.empty()) created.id = r[0]["id"].as<std::string>();
    return created;
}