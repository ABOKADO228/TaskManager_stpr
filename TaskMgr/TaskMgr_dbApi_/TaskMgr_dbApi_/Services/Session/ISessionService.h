#pragma once
#include "../Services/Interfaces/ICreateService.h"
#include "../DTO/Session/CreateSessionRequestDto.h"
class ISessionService :
	public ICreateService<std::string, CreateSessionRequestDto> 
{
public:
	virtual ~IUserService() = default;
};