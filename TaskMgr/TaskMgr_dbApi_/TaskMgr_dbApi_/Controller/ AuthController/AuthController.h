#pragma once
#include <drogon/HttpRequest.h>
#include <drogon/HttpResponse.h>
#include <functional>
#include <memory>

#include "../Services/UserService.h"

class AuthController {
public:
    explicit AuthController(std::shared_ptr<UserService> userService);

    void registerUser(const drogon::HttpRequestPtr& req,
        std::function<void(const drogon::HttpResponsePtr&)>&& cb);


    void login(const drogon::HttpRequestPtr& req,
        std::function<void(const drogon::HttpResponsePtr&)>&& cb);

private:
    std::shared_ptr<UserService> userService_;
};