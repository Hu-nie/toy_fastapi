from fastapi import APIRouter, Query
from .basketball_stats import BasketballStats
from pydantic import BaseModel, Field
from typing import Union, Optional
from datetime import date
from fastapi.responses import JSONResponse
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import threading
import logging

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get('/')
def welcome():
    """
    API 가동 상태 확인 엔드포인트.
    """
    return {'message': 'Welcome to the Basketball Stats API!'}

@router.get('/player-stats/')
def player_stats(date: date = Query(...), name: Optional[str] = None):
    """
    플레이어 통계를 조회하는 엔드포인트.
    - **date**: 조회할 날짜 (`YYYY-MM-DD` 형식).
    - **player_name**: 조회할 플레이어 이름 (선택적).
    """
    stats_scraper = BasketballStats(client, OutputType.JSON, date)
    if name:
        stats = stats_scraper.specific_player_stats(name)
    else:
        stats = stats_scraper.daily_player_stats()
    thread_id = threading.get_ident()  # 현재 스레드 ID를 가져옵니다
    logging.info(f"Handling request in thread {thread_id}")  # 로깅
    
    return JSONResponse(content=stats)

@router.get('/team_stats/')
def team_stats(date: date = Query(...), name: Optional[str] = None):
    """
    팀 통계를 조회하는 엔드포인트.
    - **date**: 조회할 날짜 (`YYYY-MM-DD` 형식).
    - **team_name**: 조회할 플레이어 이름 (선택적).
    """
    stats_scraper = BasketballStats(client, OutputType.JSON, date)

    if name:
        stats = stats_scraper.specific_team_stats(name)
    else:
        stats = stats_scraper.daily_team_stats()

    return JSONResponse(content=stats)

