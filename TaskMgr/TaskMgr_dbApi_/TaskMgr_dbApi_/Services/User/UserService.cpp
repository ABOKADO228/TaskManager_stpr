#include "UserService.h"

UserService::UserService(std::shared_ptr<IUserRepository> userRepository)
{
}

User UserService::create(const CreateUserRequestDto& dto)
{
	return User();
}

std::optional<User> UserService::getById(int id)
{
	return std::optional<User>();
}

std::vector<User> UserService::getAll()
{
	return std::vector<User>();
}

std::optional<User> UserService::update(int id, const UpdateUserRequestDto& dto)
{
	return std::optional<User>();
}

bool UserService::remove(int id)
{
	return false;
}
