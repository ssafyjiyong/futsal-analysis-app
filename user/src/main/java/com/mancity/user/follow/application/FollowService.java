package com.mancity.user.follow.application;

import com.mancity.user.follow.application.dto.request.FollowSendRequestDto;
import com.mancity.user.follow.application.dto.response.FollowResponseDto;
import com.mancity.user.follow.application.dto.response.FollowerInfo;
import com.mancity.user.follow.domain.repository.FollowRepository;
import com.mancity.user.stat.domain.MainStat;
import com.mancity.user.stat.domain.Stat;
import com.mancity.user.stat.domain.repository.StatRepository;
import com.mancity.user.user.domain.User;
import com.mancity.user.user.domain.repository.UserRepository;
import com.mancity.user.user.exception.UserNotExistException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@RequiredArgsConstructor
@Service
public class FollowService {

    private final FollowRepository followRepository;

    private final UserRepository userRepository;

    private final StatRepository statRepository;

    public void follow(FollowSendRequestDto dto) {
        followRepository.save(dto.toEntity());
    }

    public FollowResponseDto findFollowersAndFollowings(long id) {
        List<FollowerInfo> followers = findMyFollowers(id);
        List<FollowerInfo> followings = findMyFollowings(id);

        return FollowResponseDto.of(followers,followings);
    }

    public List<FollowerInfo> findMyFollowers(long id){
        List<Long> senderIds = followRepository.findSenderIdByReceiverId(id);
        List<User> senders = userRepository.findAllById(senderIds);

        List<FollowerInfo> followers = new ArrayList<>();
        for(User user : senders){
            Stat stat = statRepository.findById(user.getId()).orElseThrow(UserNotExistException::new);
            MainStat mainStat = MainStat.from(stat);
            FollowerInfo info = FollowerInfo.of(user, mainStat);

            followers.add(info);
        }

        return followers;
    }

    public List<FollowerInfo> findMyFollowings(long id){
        List<Long> receiverIds = followRepository.findReceiverIdBySenderId(id);
        List<User> receivers = userRepository.findAllById(receiverIds);

        List<FollowerInfo> followings = new ArrayList<>();
        for(User user : receivers){
            Stat stat = statRepository.findById(user.getId()).orElseThrow(UserNotExistException::new);

            MainStat mainStat = MainStat.from(stat);
            FollowerInfo info = FollowerInfo.of(user, mainStat);

            followings.add(info);
        }

        return followings;
    }
}
