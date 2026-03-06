#pragma once
#include <drogon/HttpController.h>
#include "../services/ISessionsService.h"
#include <memory>

class SessionsController : public drogon::HttpController<SessionsController>
{
public:
	explicit SessionsController(std::shared_ptr<IUserService> USerService);
	METHOD_LIST_BEGIN
		ADD_METHOD_TO(SessionsController::login, "/sessions", drogon::Post);
		ADD_METHOD_TO(SessionsController::refresh, "/sessions/refresh", drogon::Post);
		ADD_METHOD_TO(SessionsController::logout, "/sessions/logout", drogon::Post);
	METHOD_LIST_END

	void login(const drogon::HttpRequestPtr& req,
			std::function<void(const drogon::HttpResponsePtr&)>&& callback);

	void refresh(const drogon::HttpRequestPtr& req,
		std::function<void(const drogon::HttpResponsePtr&)>&& callback);

	void logout(const drogon::HttpRequestPtr& req,
		std::function<void(const drogon::HttpResponsePtr&)>&& callback);
};
private:
	std::shared_ptr<ISessionService> sessionService_;
};