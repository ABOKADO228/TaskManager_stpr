#pragma once
#include "../Services/Session/ISessionService.h"
#include "../Repository/Session/ISessionRepository.h"
#include "../DTO/Session/CreateSessionRequestDto.h"

#include <memory>
#include <string>
class SessionService : public ISessionService 
{
public:
	explicit SessionService(std::shared_ptr<ISessionRepository> sessionRepository);
	~SessionService() = default;

	std::string Create(CreateSessionRequestDto dto) override;

private:
	std::shared_ptr<ISessionRepository> sessionRepository_;
};