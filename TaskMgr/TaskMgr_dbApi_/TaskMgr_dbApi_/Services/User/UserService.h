#pragma once
#include <optional>
#include <memory>
#include "IUserService.h"
#include <vector>
#include "Repos"





class UserService final : public IUserService
{
public:
    explicit UserService(std::shared_ptr<IUserRepository> userRepository);
    ~UserService() override = default;

public:
    User create(const CreateUserRequestDto& dto) override;
    std::optional<User> getById(int id) override;
    std::vector<User> getAll() override;
    std::optional<User> update(int id, const UpdateUserRequestDto& dto) override;
    bool remove(int id) override;

private:
    std::shared_ptr<IUserRepository> userRepository_;
};