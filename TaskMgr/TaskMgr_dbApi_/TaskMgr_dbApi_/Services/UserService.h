#pragma once
#include <memory>
#include <string>

#include "../Domain/Interfaces/IUserRepository.h"
#include "../DTO/RegisterRequest.h"
#include "../DTO/LoginRequest.h"
#include "../DTO/UserResponse.h"

class UserService {
public:
    explicit UserService(std::shared_ptr<IUserRepository> repo);

    UserResponse registerUser(const RegisterRequest& req);
    bool login(const LoginRequest& req);

private:
    std::shared_ptr<IUserRepository> repo_;

    static std::string hashPassword(const std::string& pwd);
    static bool verifyPassword(const std::string& pwd, const std::string& hash);
};