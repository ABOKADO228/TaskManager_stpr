#include "SessionsController.h"

SessionsController::SessionsController(std::shared_ptr<IUserService> USerService)
{
	 
}

void SessionsController::login(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback)
{
}

void SessionsController::createAccessToken(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback)
{
}

void SessionsController::logout(const drogon::HttpRequestPtr& req, std::function<void(const drogon::HttpResponsePtr&)>&& callback)
{
}
