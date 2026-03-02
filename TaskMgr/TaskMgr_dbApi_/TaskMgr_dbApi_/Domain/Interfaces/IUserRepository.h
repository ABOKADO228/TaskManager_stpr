#pragma once
#include <optional>
#include "../Models/UserModel.h"

class IUserRepository {
public:
    virtual ~IUserRepository() = default;

    virtual User create(const User& u) = 0;
    virtual std::optional<User> findByLogin(const std::string& login) = 0;
    virtual std::optional<User> findByEmail(const std::string& email) = 0;
};