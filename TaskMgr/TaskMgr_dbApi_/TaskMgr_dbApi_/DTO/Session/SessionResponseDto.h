#pragma once
#include <string>
#include <json/json.h>

struct SessionResponseDto
{
    std::string userId;
    std::string accessToken;
    std::string refreshToken;
    std::string refreshExpiresAt;

    Json::Value toJson() const
    {
        Json::Value json;
        json["userId"] = userId;
        json["accessToken"] = accessToken;
        json["refreshToken"] = refreshToken;
        json["refreshExpiresAt"] = refreshExpiresAt;
        return json;
    }
};