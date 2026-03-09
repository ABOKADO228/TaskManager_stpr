#include "SessionsController.h"

SessionsController::SessionsController(std::shared_ptr<ISessionService> USerService)
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
