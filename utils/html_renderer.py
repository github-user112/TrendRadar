from typing import Dict, Optional
from datetime import datetime
from .html_escape import html_escape
from .time_utils import get_beijing_time


def render_html_content(
    report_data: Dict,
    total_titles: int,
    is_daily_summary: bool = False,
    mode: str = "daily",
    update_info: Optional[Dict] = None,
) -> str:
    """渲染HTML内容"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>热点新闻分析</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js" integrity="sha512-BNaRQnYJYiPSqHHDb58B0yaPfCu+Wgds8Gp/gU33kqBtgNS4tSPHuGibyoeqMV/TJlSKda6FXzoEyYGjTe+vXA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                margin: 0; 
                padding: 16px;
                background: #f5f5f5;
                color: #333333;
                line-height: 1.4;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 24px rgba(0,0,0,0.1);
            }
            
            .header {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                color: white;
                padding: 24px;
                text-align: center;
                position: relative;
            }
            
            .save-buttons {
                position: absolute;
                top: 12px;
                right: 12px;
                display: flex;
                gap: 8px;
            }
            
            .save-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
                font-weight: 500;
                transition: all 0.2s ease;
                backdrop-filter: blur(10px);
                white-space: nowrap;
            }
            
            .save-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.5);
                transform: translateY(-1px);
            }
            
            .save-btn:active {
                transform: translateY(0);
            }
            
            .save-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .header-title {
                font-size: 20px;
                font-weight: 700;
                margin: 0 0 16px 0;
            }
            
            .header-info {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1fr;
                gap: 12px;
                font-size: 13px;
                opacity: 0.95;
            }
            
            .info-item {
                text-align: center;
            }
            
            .info-label {
                display: block;
                font-size: 11px;
                opacity: 0.8;
                margin-bottom: 2px;
            }
            
            .info-value {
                font-weight: 600;
                font-size: 14px;
            }
            
            .content {
                padding: 20px;
            }
            
            /* 新增热点区域 */
            .new-section {
                margin-bottom: 32px;
                padding: 20px;
                background: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            
            .new-section-title {
                color: #333333;
                font-size: 16px;
                font-weight: 600;
                margin: 0 0 16px 0;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .new-section-title::before {
                content: "🔥";
                font-size: 18px;
            }
            
            /* 新增热点平台卡片容器 */
            .new-platforms-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 16px;
            }
            
            /* 新增热点平台卡片 */
            .new-platform-card {
                background: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
                transition: all 0.2s ease;
            }
            
            .new-platform-card:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border-color: #d0d0d0;
            }
            
            .new-source-title {
                color: #666666;
                font-size: 14px;
                font-weight: 600;
                margin: 0 0 12px 0;
                padding-bottom: 6px;
                border-bottom: 2px solid #f0f0f0;
            }
            
            .new-item {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 8px 0;
                border-bottom: 1px solid #f0f0f0;
                font-size: 13px;
            }
            
            .new-item:last-child {
                border-bottom: none;
            }
            
            .new-item-number {
                color: #999999;
                font-size: 11px;
                font-weight: 600;
                min-width: 16px;
                text-align: center;
                flex-shrink: 0;
                background: #f0f0f0;
                border-radius: 50%;
                width: 18px;
                height: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 2px;
            }
            
            .new-item-rank {
                color: #fff;
                background: #999999;
                font-size: 9px;
                font-weight: 700;
                padding: 2px 5px;
                border-radius: 6px;
                min-width: 18px;
                text-align: center;
                flex-shrink: 0;
                margin-top: 2px;
            }
            
            .new-item-rank.top { background: #dc2626; }
            .new-item-rank.high { background: #ea580c; }
            
            .new-item-content {
                flex: 1;
                min-width: 0;
            }
            
            .new-item-title {
                font-size: 13px;
                line-height: 1.4;
                color: #333333;
                margin: 0;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            /* 平台卡片容器 */
            .platforms-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 16px;
            }
            
            /* 平台卡片样式 */
            .platform-card {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                overflow: hidden;
                transition: all 0.2s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            
            .platform-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(0,0,0,0.1);
                border-color: #d0d0d0;
            }
            
            /* 平台标题栏 */
            .platform-header {
                padding: 12px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-weight: 600;
                font-size: 14px;
            }
            
            /* 平台特定颜色 */
            .platform-card.toutiao .platform-header { background: #ff6b35; color: white; }
            .platform-card.baidu .platform-header { background: #317ef3; color: white; }
            .platform-card.weibo .platform-header { background: #e6162d; color: white; }
            .platform-card.douyin .platform-header { background: #fe2c55; color: white; }
            .platform-card.zhihu .platform-header { background: #0084ff; color: white; }
            .platform-card.bilibili .platform-header { background: #00a1d6; color: white; }
            .platform-card.tieba .platform-header { background: #f15a22; color: white; }
            .platform-card.ifeng .platform-header { background: #ce0000; color: white; }
            .platform-card.wallstreetcn .platform-header { background: #f0f0f0; color: #00b42a; border-bottom: 1px solid #e0e0e0; }
            .platform-card.cls .platform-header { background: #009966; color: white; }
            .platform-card.default .platform-header { background: #9e9e9e; color: white; }
            
            .platform-title {
                margin: 0;
                font-size: 14px;
                font-weight: 600;
            }
            
            .platform-stats {
                font-size: 11px;
                opacity: 0.9;
            }
            
            /* 新闻列表 - 添加滚动条 */
            .platform-news {
                padding: 12px 16px;
                max-height: 400px;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: #c0c0c0 #f0f0f0;
            }
            
            /* 滚动条样式 */
            .platform-news::-webkit-scrollbar {
                width: 6px;
            }
            
            .platform-news::-webkit-scrollbar-track {
                background: #f0f0f0;
                border-radius: 3px;
            }
            
            .platform-news::-webkit-scrollbar-thumb {
                background: #c0c0c0;
                border-radius: 3px;
            }
            
            .platform-news::-webkit-scrollbar-thumb:hover {
                background: #a0a0a0;
            }
            
            /* 新闻项 */
            .news-item {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 10px 0;
                border-bottom: 1px solid #e8e8e8;
                font-size: 14px;
                line-height: 1.5;
                transition: background-color 0.2s ease;
            }
            
            .news-item:hover {
                background-color: #fafafa;
            }
            
            .news-item:last-child {
                border-bottom: none;
            }
            
            .news-rank {
                color: #666666;
                font-size: 12px;
                font-weight: 600;
                min-width: 20px;
                text-align: right;
                flex-shrink: 0;
                margin-top: 2px;
            }
            
            .news-rank.top { color: #e53935; font-weight: 700; }
            .news-rank.high { color: #f57c00; font-weight: 700; }
            
            .news-content {
                flex: 1;
                min-width: 0;
            }
            
            .news-title {
                font-size: 14px;
                color: #212121;
                margin: 0 0 5px 0;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
                font-weight: 500;
            }
            
            .news-title a {
                color: #212121 !important;
                text-decoration: none !important;
                transition: color 0.2s ease;
            }
            
            .news-title a:hover {
                color: #1976d2 !important;
                text-decoration: underline !important;
            }
            
            .news-meta {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 11px;
                color: #757575;
            }
            
            .news-source {
                color: #616161;
                font-weight: 600;
            }
            
            .news-time {
                color: #9e9e9e;
            }
            
            .news-count {
                color: #43a047;
                font-weight: 600;
            }
            
            /* 错误信息 */
            .error-section {
                background: #fff8f8;
                border: 1px solid #ffcccc;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 24px;
            }
            
            .error-title {
                color: #dc2626;
                font-size: 13px;
                font-weight: 600;
                margin: 0 0 8px 0;
            }
            
            .error-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            
            .error-item {
                color: #b00020;
                font-size: 12px;
                padding: 2px 0;
                font-family: 'SF Mono', Consolas, monospace;
            }
            
            /* 页脚 */
            .footer {
                margin-top: 24px;
                padding: 16px 20px;
                background: #fafafa;
                border-top: 1px solid #e0e0e0;
                text-align: center;
            }
            
            .footer-content {
                font-size: 12px;
                color: #666666;
                line-height: 1.4;
            }
            
            .footer-link {
                color: #2196f3;
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s ease;
            }
            
            .footer-link:hover {
                color: #1976d2;
                text-decoration: underline;
            }
            
            .project-name {
                font-weight: 600;
                color: #333333;
            }
            
            /* 响应式设计 */
            @media (max-width: 1200px) {
                .platforms-container,
                .new-platforms-container {
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 12px;
                }
            }
            
            @media (max-width: 768px) {
                body { padding: 12px; }
                .container { border-radius: 8px; }
                .header { padding: 20px; }
                .content { padding: 16px; }
                .platforms-container,
                .new-platforms-container {
                    grid-template-columns: 1fr;
                    gap: 12px;
                }
                .header-info {
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                }
                .save-buttons {
                    position: static;
                    margin-bottom: 12px;
                    display: flex;
                    gap: 8px;
                    justify-content: center;
                }
            }
            
            @media (max-width: 480px) {
                .header-info {
                    grid-template-columns: 1fr;
                    gap: 8px;
                }
                .save-buttons {
                    flex-direction: column;
                }
                .save-btn {
                    width: 100%;
                }
                .new-item {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 4px;
                }
                .news-item {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 4px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="save-buttons">
                    <button class="save-btn" onclick="saveAsImage()">保存为图片</button>
                    <button class="save-btn" onclick="saveAsMultipleImages()">分段保存</button>
                </div>
                <div class="header-title">热点新闻分析</div>
                <div class="header-info">
                    <div class="info-item">
                        <span class="info-label">报告类型</span>
                        <span class="info-value">"""

    # 处理报告类型显示
    if is_daily_summary:
        if mode == "current":
            html += "当前榜单"
        elif mode == "incremental":
            html += "增量模式"
        else:
            html += "当日汇总"
    else:
        html += "实时分析"

    html += """
                    </span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">新闻总数</span>
                        <span class="info-value">"""

    html += f"{total_titles} 条"

    # 计算筛选后的热点新闻数量
    hot_news_count = sum(len(stat["titles"]) for stat in report_data["stats"])

    html += """
                    </span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">热点新闻</span>
                        <span class="info-value">"""

    html += f"{hot_news_count} 条"

    html += """
                    </span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">生成时间</span>
                        <span class="info-value">"""

    now = get_beijing_time()
    html += now.strftime("%m-%d %H:%M")

    html += """
                    </span>
                    </div>
                </div>
            </div>
            
            <div class="content">"""

    # 处理失败ID错误信息
    if report_data["failed_ids"]:
        html += """
                <div class="error-section">
                    <div class="error-title">⚠️ 请求失败的平台</div>
                    <ul class="error-list">"""
        for id_value in report_data["failed_ids"]:
            html += f'<li class="error-item">{html_escape(id_value)}</li>'
        html += """
                    </ul>
                </div>"""

    # 处理新增新闻区域（放在上面）
    if report_data["new_titles"]:
        html += f"""
                <div class="new-section">
                    <div class="new-section-title">本次新增热点 (共 {report_data['total_new_count']} 条)</div>
                    <div class="new-platforms-container">"""

        for source_data in report_data["new_titles"]:
            escaped_source = html_escape(source_data["source_name"])
            titles_count = len(source_data["titles"])

            html += f"""
                        <div class="new-platform-card">
                            <div class="new-source-title">{escaped_source} · {titles_count}条</div>"""

            # 为新增新闻也添加序号
            for idx, title_data in enumerate(source_data["titles"], 1):
                ranks = title_data.get("ranks", [])

                # 处理新增新闻的排名显示
                rank_class = ""
                if ranks:
                    min_rank = min(ranks)
                    if min_rank <= 3:
                        rank_class = "top"
                    elif min_rank <= title_data.get("rank_threshold", 10):
                        rank_class = "high"

                    if len(ranks) == 1:
                        rank_text = str(ranks[0])
                    else:
                        rank_text = f"{min(ranks)}-{max(ranks)}"
                else:
                    rank_text = "?"

                html += f"""
                            <div class="new-item">
                                <div class="new-item-number">{idx}</div>
                                <div class="new-item-rank {rank_class}">{rank_text}</div>
                                <div class="new-item-content">
                                    <div class="new-item-title">"""

                # 处理新增新闻的链接
                escaped_title = html_escape(title_data["title"])
                link_url = title_data.get("mobile_url") or title_data.get("url", "")

                if link_url:
                    escaped_url = html_escape(link_url)
                    html += f'<a href="{escaped_url}" target="_blank" style="color: #2196f3; text-decoration: none;">{escaped_title}</a>'
                else:
                    html += escaped_title

                html += """
                                    </div>
                                </div>
                            </div>"""

            html += """
                        </div>"""

        html += """
                    </div>
                </div>"""

    # 按平台分组所有新闻
    all_platform_news = {}
    for stat in report_data["stats"]:
        for title_data in stat["titles"]:
            source_name = title_data["source_name"]
            if source_name not in all_platform_news:
                all_platform_news[source_name] = []
            all_platform_news[source_name].append(title_data)
    
    # 处理主要统计数据 - 按平台卡片展示
    if all_platform_news:
        # 平台名称映射到CSS类名
        platform_css_map = {
            "今日头条": "toutiao",
            "百度热搜": "baidu",
            "微博": "weibo",
            "抖音": "douyin",
            "知乎": "zhihu",
            "bilibili 热搜": "bilibili",
            "贴吧": "tieba",
            "凤凰网": "ifeng",
            "华尔街见闻": "wallstreetcn",
            "财联社热门": "cls"
        }
        
        html += """
                <div class="platforms-container">"""
        
        # 遍历每个平台，创建平台卡片
        for platform, titles in all_platform_news.items():
            total = len(titles)
            show_more = total > 10
            visible_titles = titles[:10]
            hidden_titles = titles[10:]
            
            # 生成唯一的平台ID用于标识
            platform_id = f"platform-{platform.replace(' ', '-').lower()}"
            
            # 获取平台对应的CSS类名
            platform_css = platform_css_map.get(platform, "default")
            
            html += f"""
                    <div class="platform-card {platform_css}">
                        <div class="platform-header">
                            <h3 class="platform-title">{html_escape(platform)}</h3>
                            <span class="platform-stats">{total} 条</span>
                        </div>
                        <div class="platform-news">"""
            
            # 显示所有新闻
            for idx, title_data in enumerate(titles, 1):
                is_new = title_data.get("is_new", False)
                
                # 处理排名显示
                ranks = title_data.get("ranks", [])
                rank_text = ""
                rank_class = ""
                if ranks:
                    min_rank = min(ranks)
                    if min_rank <= 3:
                        rank_class = "top"
                    elif min_rank <= title_data.get("rank_threshold", 10):
                        rank_class = "high"
                    
                    if len(ranks) == 1:
                        rank_text = str(ranks[0])
                    else:
                        rank_text = f"{min(ranks)}-{max(ranks)}"
                
                # 处理时间显示
                time_display = title_data.get("time_display", "")
                if time_display:
                    simplified_time = time_display.replace(" ~ ", "~").replace("[", "").replace("]", "")
                
                # 处理出现次数
                count_info = title_data.get("count", 1)
                
                # 处理标题和链接
                escaped_title = html_escape(title_data["title"])
                link_url = title_data.get("mobile_url") or title_data.get("url", "")
                
                html += f"""
                            <div class="news-item">
                                <div class="news-rank {rank_class}">{rank_text}</div>
                                <div class="news-content">
                                    <div class="news-title">"""
                
                if link_url:
                    escaped_url = html_escape(link_url)
                    html += f'<a href="{escaped_url}" target="_blank">{escaped_title}</a>'
                else:
                    html += escaped_title
                
                html += f"""
                                    </div>
                                    <div class="news-meta">"""
                
                if time_display:
                    html += f'<span class="news-time">{html_escape(simplified_time)}</span>'
                
                if count_info > 1:
                    html += f'<span class="news-count">{count_info}次</span>'
                
                html += f"""
                                    </div>
                                </div>
                            </div>"""
            
            html += f"""
                        </div>"""
            
            html += f"""
                    </div>"""
        
        html += """
                </div>"""

    html += """
            </div>
            
            <div class="footer">
                <div class="footer-content">
                    由 <span class="project-name">TrendRadar</span> 生成 · 
                    <a href="https://github.com/sansan0/TrendRadar" target="_blank" class="footer-link">
                        GitHub 开源项目
                    </a>"""

    if update_info:
        html += f"""
                    <br>
                    <span style="color: #ea580c; font-weight: 500;">
                        发现新版本 {update_info['remote_version']}，当前版本 {update_info['current_version']}
                    </span>"""

    html += """
                </div>
            </div>
        </div>
        
        <script>
            // 切换显示/隐藏更多新闻
            function toggleNews(platformId, total) {
                const button = event.target;
                const hiddenContainer = document.getElementById(`${platformId}-hidden`);
                const hiddenGrid = document.getElementById(`${platformId}-hidden-grid`);
                
                if (hiddenContainer.style.display === 'none') {
                    // 显示隐藏的新闻
                    hiddenContainer.style.display = 'block';
                    button.textContent = '收起';
                } else {
                    // 隐藏新闻
                    hiddenContainer.style.display = 'none';
                    button.textContent = `查看更多 (${total - 10} 条)`;
                }
            }
            
            async function saveAsImage() {
                const button = event.target;
                const originalText = button.textContent;
                
                try {
                    button.textContent = '生成中...';
                    button.disabled = true;
                    window.scrollTo(0, 0);
                    
                    // 等待页面稳定
                    await new Promise(resolve => setTimeout(resolve, 200));
                    
                    // 截图前隐藏按钮
                    const buttons = document.querySelector('.save-buttons');
                    buttons.style.visibility = 'hidden';
                    
                    // 再次等待确保按钮完全隐藏
                    await new Promise(resolve => setTimeout(resolve, 100));
                    
                    const container = document.querySelector('.container');
                    
                    const canvas = await html2canvas(container, {
                        backgroundColor: '#ffffff',
                        scale: 1.5,
                        useCORS: true,
                        allowTaint: false,
                        imageTimeout: 10000,
                        removeContainer: false,
                        foreignObjectRendering: false,
                        logging: false,
                        width: container.offsetWidth,
                        height: container.offsetHeight,
                        x: 0,
                        y: 0,
                        scrollX: 0,
                        scrollY: 0,
                        windowWidth: window.innerWidth,
                        windowHeight: window.innerHeight
                    });
                    
                    buttons.style.visibility = 'visible';
                    
                    const link = document.createElement('a');
                    const now = new Date();
                    const filename = `TrendRadar_热点新闻分析_${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}.png`;
                    
                    link.download = filename;
                    link.href = canvas.toDataURL('image/png', 1.0);
                    
                    // 触发下载
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    button.textContent = '保存成功!';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);
                    
                } catch (error) {
                    const buttons = document.querySelector('.save-buttons');
                    buttons.style.visibility = 'visible';
                    button.textContent = '保存失败';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);
                }
            }
            
            async function saveAsMultipleImages() {
                const button = event.target;
                const originalText = button.textContent;
                const container = document.querySelector('.container');
                const scale = 1.5; 
                const maxHeight = 5000 / scale;
                
                try {
                    button.textContent = '分析中...';
                    button.disabled = true;
                    
                    // 获取所有可能的分割元素
                    const newsItems = Array.from(container.querySelectorAll('.news-item, .news-card'));
                    const wordGroups = Array.from(container.querySelectorAll('.word-group'));
                    const newSection = container.querySelector('.new-section');
                    const errorSection = container.querySelector('.error-section');
                    const header = container.querySelector('.header');
                    const footer = container.querySelector('.footer');
                    
                    // 计算元素位置和高度
                    const containerRect = container.getBoundingClientRect();
                    const elements = [];
                    
                    // 添加header作为必须包含的元素
                    elements.push({
                        type: 'header',
                        element: header,
                        top: 0,
                        bottom: header.offsetHeight,
                        height: header.offsetHeight
                    });
                    
                    // 添加错误信息（如果存在）
                    if (errorSection) {
                        const rect = errorSection.getBoundingClientRect();
                        elements.push({
                            type: 'error',
                            element: errorSection,
                            top: rect.top - containerRect.top,
                            bottom: rect.bottom - containerRect.top,
                            height: rect.height
                        });
                    }
                    
                    // 按word-group分组处理news-item
                    wordGroups.forEach(group => {
                        const groupRect = group.getBoundingClientRect();
                        const groupNewsItems = group.querySelectorAll('.news-item, .news-card');
                        
                        // 添加word-group的header部分
                        const wordHeader = group.querySelector('.word-header');
                        if (wordHeader) {
                            const headerRect = wordHeader.getBoundingClientRect();
                            elements.push({
                                type: 'word-header',
                                element: wordHeader,
                                top: headerRect.top - containerRect.top,
                                bottom: headerRect.bottom - containerRect.top,
                                height: headerRect.height
                            });
                        }
                        
                        // 添加平台分组
                        const platformGroups = group.querySelectorAll('.platform-group');
                        platformGroups.forEach(platformGroup => {
                            const platformRect = platformGroup.getBoundingClientRect();
                            elements.push({
                                type: 'platform-group',
                                element: platformGroup,
                                top: platformRect.top - containerRect.top,
                                bottom: platformRect.bottom - containerRect.top,
                                height: platformRect.height
                            });
                        });
                        
                        // 添加新闻项
                        groupNewsItems.forEach(item => {
                            const rect = item.getBoundingClientRect();
                            elements.push({
                                type: 'news-item',
                                element: item,
                                top: rect.top - containerRect.top,
                                bottom: rect.bottom - containerRect.top,
                                height: rect.height
                            });
                        });
                    });
                    
                    // 添加new-section（如果存在）
                    if (newSection) {
                        const rect = newSection.getBoundingClientRect();
                        elements.push({
                            type: 'new-section',
                            element: newSection,
                            top: rect.top - containerRect.top,
                            bottom: rect.bottom - containerRect.top,
                            height: rect.height
                        });
                    }
                    
                    // 添加footer作为必须包含的元素
                    elements.push({
                        type: 'footer',
                        element: footer,
                        top: container.offsetHeight - footer.offsetHeight,
                        bottom: container.offsetHeight,
                        height: footer.offsetHeight
                    });
                    
                    // 按top值排序
                    elements.sort((a, b) => a.top - b.top);
                    
                    // 计算分割点
                    const segments = [];
                    let currentSegment = {
                        elements: [],
                        height: 0,
                        startIndex: 0
                    };
                    
                    // 确保header在第一个分段
                    const headerElement = elements.find(e => e.type === 'header');
                    if (headerElement) {
                        currentSegment.elements.push(headerElement);
                        currentSegment.height += headerElement.height;
                    }
                    
                    // 遍历元素，构建分段
                    for (let i = 1; i < elements.length; i++) {
                        const element = elements[i];
                        
                        // 如果添加当前元素不会超过最大高度，则添加到当前分段
                        if (currentSegment.height + element.height <= maxHeight) {
                            currentSegment.elements.push(element);
                            currentSegment.height += element.height;
                        } else {
                            // 保存当前分段
                            segments.push(currentSegment);
                            
                            // 开始新的分段
                            currentSegment = {
                                elements: [element],
                                height: element.height,
                                startIndex: i
                            };
                        }
                    }
                    
                    // 添加最后一个分段
                    if (currentSegment.elements.length > 0) {
                        segments.push(currentSegment);
                    }
                    
                    // 生成图片
                    button.textContent = `生成中 (1/${segments.length})`;
                    
                    for (let i = 0; i < segments.length; i++) {
                        const segment = segments[i];
                        
                        // 更新按钮文本
                        button.textContent = `生成中 (${i + 1}/${segments.length})`;
                        
                        // 隐藏所有元素
                        container.querySelectorAll('*').forEach(el => {
                            el.style.visibility = 'hidden';
                        });
                        
                        // 只显示当前分段的元素
                        segment.elements.forEach(el => {
                            el.element.style.visibility = 'visible';
                            
                            // 确保所有父元素也可见
                            let parent = el.element.parentElement;
                            while (parent && parent !== container) {
                                parent.style.visibility = 'visible';
                                parent = parent.parentElement;
                            }
                        });
                        
                        // 等待页面稳定
                        await new Promise(resolve => setTimeout(resolve, 200));
                        
                        // 隐藏按钮
                        const buttons = document.querySelector('.save-buttons');
                        buttons.style.visibility = 'hidden';
                        
                        // 生成截图
                        const canvas = await html2canvas(container, {
                            backgroundColor: '#ffffff',
                            scale: scale,
                            useCORS: true,
                            allowTaint: false,
                            imageTimeout: 10000,
                            removeContainer: false,
                            foreignObjectRendering: false,
                            logging: false,
                            width: container.offsetWidth,
                            height: container.offsetHeight,
                            x: 0,
                            y: 0,
                            scrollX: 0,
                            scrollY: 0,
                            windowWidth: window.innerWidth,
                            windowHeight: window.innerHeight
                        });
                        
                        // 恢复所有元素可见性
                        container.querySelectorAll('*').forEach(el => {
                            el.style.visibility = '';
                        });
                        
                        // 下载图片
                        const link = document.createElement('a');
                        const now = new Date();
                        const filename = `TrendRadar_热点新闻分析_${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}_${i + 1}.png`;
                        
                        link.download = filename;
                        link.href = canvas.toDataURL('image/png', 1.0);
                        
                        // 触发下载
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        
                        // 等待下载完成
                        await new Promise(resolve => setTimeout(resolve, 500));
                    }
                    
                    button.textContent = '全部保存成功!';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);
                    
                } catch (error) {
                    // 恢复所有元素可见性
                    container.querySelectorAll('*').forEach(el => {
                        el.style.visibility = '';
                    });
                    
                    button.textContent = '保存失败';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);
                }
            }
        </script>
    </body>
    </html>
    """
    return html
