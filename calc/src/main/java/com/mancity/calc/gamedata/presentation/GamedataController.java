package com.mancity.calc.gamedata.presentation;

import com.mancity.calc.gamedata.application.GamedataService;
import com.mancity.calc.gamedata.application.dto.request.GamedataRequestDto;
import com.mancity.calc.social.application.dto.request.CreateHighlightRequestDto;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;


@Controller
@RequiredArgsConstructor
@RequestMapping("/api/calc")
public class GamedataController {

    private final GamedataService gamedataService;

    @PostMapping("/gamedata")
    @Operation(summary = "영상 처리 결과 데이터 받기", description = "분석을 위한 영상 처리 데이터를 제공받습니다")
    public ResponseEntity<?> getTrackData(@RequestBody GamedataRequestDto dto) {
        gamedataService.putDataIntoAlgorithm(dto);
        return new ResponseEntity<>(HttpStatus.OK);



    }

    @PostMapping("/createHighlights")
    @Operation(summary = "하이라이트 생성", description = "경기의 모든 하이라이트를 생성합니다.")
    public ResponseEntity<?> createHighlights(@RequestBody CreateHighlightRequestDto dto) {
        gamedataService.createHighlights(dto);
        return new ResponseEntity<>(HttpStatus.OK);
    }

}
