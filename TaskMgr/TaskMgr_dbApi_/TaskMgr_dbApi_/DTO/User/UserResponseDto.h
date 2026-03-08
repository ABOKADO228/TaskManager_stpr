#pragma once
#include <string>
#include <optional>
#include <json/json.h>


struct UserResponseDto {
	int id;
	std::string login;
	std::string email;
	Json::Value toJson() const {
		Json::Value json;
		json["id"] = id;
		json["email"] = email;
		json["login"] = login;
		return json;
	}
};