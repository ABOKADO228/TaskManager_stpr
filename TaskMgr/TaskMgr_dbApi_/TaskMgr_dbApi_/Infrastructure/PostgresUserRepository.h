#pragma once
#include <pqxx/pqxx>
#include "../Domain/Interfaces/IUserRepository.h"
#include "DbConfig.h"

class PostgresUserRepository : public IUserRepository {
public:
    explicit PostgresUserRepository(const DbConfig& cfg);

    User create(const User& u) override;
    std::optional<User> findByLogin(const std::string& login) override;
    std::optional<User> findByEmail(const std::string& email) override;

private:
    std::string connStr_;
    static User mapRow(const pqxx::row& r);
};