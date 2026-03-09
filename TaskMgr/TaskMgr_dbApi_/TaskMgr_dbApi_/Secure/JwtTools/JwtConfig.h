namespace jwtConf {
	static const std::string kJwtSecret = "change-me-super-secret-key";
	static const std::string kJwtIssuer = "drogon-auth-service";
	static const std::string kJwtAudience = "drogon-api";

	static constexpr int kAccessTtlSec = 15 * 60;
	static constexpr int kRefreshTtlSec = 30 * 24 * 3600;
}