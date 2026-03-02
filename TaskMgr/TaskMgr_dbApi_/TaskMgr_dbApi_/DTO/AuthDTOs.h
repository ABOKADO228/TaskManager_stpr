#pragma once
#include <drogon/drogon.h>

struct RegisterRequestDto {
    std::string email;
    std::string login;
    std::string password;

    static std::optional<RegisterRequestDto> fromJson(const Json::Value& j) {
        if (!j.isObject()) return std::nullopt;
        if (!j.isMember("email") || !j.isMember("login") || !j.isMember("password")) return std::nullopt;

        RegisterRequestDto d;
        d.email = j["email"].asString();
        d.login = j["login"].asString();
        d.password = j["password"].asString();
        return d;
    }
};

struct LoginRequestDto {
    std::string login;
    std::string password;

    static std::optional<LoginRequestDto> fromJson(const Json::Value& j) {
        if (!j.isObject()) return std::nullopt;
        if (!j.isMember("login") || !j.isMember("password")) return std::nullopt;

        LoginRequestDto d;
        d.login = j["login"].asString();
        d.password = j["password"].asString();
        return d;
    }
};

struct AuthResponseDto {
    // пока без JWT: просто “кто вошёл”
    long long userId{};
    std::string login;
    std::string email;

    Json::Value toJson() const {
        Json::Value j;
        j["userId"] = Json::Int64(userId);
        j["login"] = login;
        j["email"] = email;
        return j;
    }
};