#pragma once

#include "../Interfaces/ICreateService.h"
#include "../Interfaces/IGetByIdService.h"
#include "../Interfaces/IGetAllService.h"
#include "../Interfaces/IUpdateService.h"
#include "../Interfaces/IDeleteService.h"
#include "../../DTO/User/CreateUserRequestDto.h"
#include "../../DTO/User/UpdateUserRequestDto.h"
#include "../../Models/User.h"

#include <optional>

class IUserService :
    public ICreateService<User, CreateUserRequestDto>,
    public IGetByIdService<User, int>,
    public IGetAllService<User>,
    public IUpdateService<User, UpdateUserRequestDto>,
    public IDeleteService<int>
{
public:
    virtual ~IUserService() = default;
};