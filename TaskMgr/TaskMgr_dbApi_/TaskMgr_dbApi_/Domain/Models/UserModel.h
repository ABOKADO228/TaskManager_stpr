#pragma once
#include <string>
#include <optional>

struct User {
    long long id{};
    std::string email;
    std::string login;
    std::string passwordHash;
    std::optional<std::string> createdAt;
};