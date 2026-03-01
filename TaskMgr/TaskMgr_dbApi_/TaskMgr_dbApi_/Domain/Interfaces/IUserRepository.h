#pragma once
#include <optional>
#include <string>
#include "../Models/User.h"

class IUserRepository {
public:
    virtual ~IUserRepository() = default;

    virtual bool usernameExists(const std::string& username) = 0;
    virtual User create(const User& user) = 0;
    virtual std::optional<User> findByUsername(const std::string& username) = 0;
};