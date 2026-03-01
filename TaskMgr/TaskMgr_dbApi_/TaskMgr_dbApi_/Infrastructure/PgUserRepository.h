#pragma once
#include "../Domain/Interfaces/IUserRepository.h"
#include <drogon/orm/DbClient.h>

class PgUserRepository final : public IUserRepository {
public:
    explicit PgUserRepository(drogon::orm::DbClientPtr db);

    bool usernameExists(const std::string& username) override;
    User create(const User& user) override;
    std::optional<User> findByUsername(const std::string& username) override;

private:
    drogon::orm::DbClientPtr db_;
};