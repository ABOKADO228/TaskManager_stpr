#pragma once
#include <optional>
#include <string>
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

		CreateUserRequestDto dto;
		dto.email = json["email"].asString();
		dto.login = json["login"].asString();
		dto.password = json["password"].asString();

		return dto;
	}
};