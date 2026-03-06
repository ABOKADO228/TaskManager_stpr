#pragma once
#include <string>
#include <optional>
#include <drogon/drogon.h>
#include <json/json.h>

struct CreateUserRequestDto
{
	std::string login;
	std::string password;
	std::string email;

	static std::optional<CreateUserRequestDto> fromJson(const Json::Value& json)
	{
		if (!json.isObject())
			return std::nullopt;

		if (!json.isMember("email") || !json["email"].isString())
			return std::nullopt;

		if (!json.isMember("login") || !json["login"].isString())
			return std::nullopt;

		if (!json.isMember("password") || !json["password"].isString())
			return std::nullopt;
	}
};