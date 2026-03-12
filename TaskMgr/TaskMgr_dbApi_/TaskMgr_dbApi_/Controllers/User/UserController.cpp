#include "UserController.h"
#include "../dto/CreateUserRequest.h"
#include "../dto/UserResponse.h"

using namespace drogon;

UserController::UserController(std::shared_ptr<IUserService> userService)
    : userService_(std::move(userService))
{
}

void UserController::getAll(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback)
{
}

void UserController::getById(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback, int id)
{

}

void UserController::create(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback)
{
}

void UserController::update(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback, int id)
{
}

void UserController::remove(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback, int id)
{
}
