#pragma once
#include <drogon/HttpController.h>
#include "../services/IUserService.h"
#include <memory>


class UserController : public drogon::HttpController<UserController>
{
public:
    explicit UserController(std::shared_ptr<IUserService> USerService);
    METHOD_LIST_BEGIN
        ADD_METHOD_TO(UserController::getAll, "/api/users", drogon::Get);
        ADD_METHOD_TO(UserController::getById, "/api/users/{1}", drogon::Get);
        ADD_METHOD_TO(UserController::create, "/api/users", drogon::Post);
        ADD_METHOD_TO(UserController::update, "/api/users/{1}", drogon::Put);
        ADD_METHOD_TO(UserController::remove, "/api/users/{1}", drogon::Delete);
    METHOD_LIST_END
        void getAll(const drogon::HttpRequestPtr& req,
            std::function<void(const drogon::HttpResponsePtr&)>&& callback);

    void getById(const drogon::HttpRequestPtr& req,
        std::function<void(const drogon::HttpResponsePtr&)>&& callback,
        int id);

    void create(const drogon::HttpRequestPtr& req,
        std::function<void(const drogon::HttpResponsePtr&)>&& callback);

    void update(const drogon::HttpRequestPtr& req,
        std::function<void(const drogon::HttpResponsePtr&)>&& callback,
        int id);

    void remove(const drogon::HttpRequestPtr& req,
        std::function<void(const drogon::HttpResponsePtr&)>&& callback,
        int id);

private:
    std::shared_ptr<IUserService> userService_;
};
