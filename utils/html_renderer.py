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
                background: #fafafa;
                color: #333;
                line-height: 1.5;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 16px rgba(0,0,0,0.06);
            }
            
            .header {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                color: white;
                padding: 32px 24px;
                text-align: center;
                position: relative;
            }
            
            .save-buttons {
                position: absolute;
                top: 16px;
                right: 16px;
                display: flex;
                gap: 8px;
            }
            
            .save-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
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
                font-size: 22px;
                font-weight: 700;
                margin: 0 0 20px 0;
            }
            
            .header-info {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1fr;
                gap: 16px;
                font-size: 14px;
                opacity: 0.95;
            }
            
            .info-item {
                text-align: center;
            }
            
            .info-label {
                display: block;
                font-size: 12px;
                opacity: 0.8;
                margin-bottom: 4px;
            }
            
            .info-value {
                font-weight: 600;
                font-size: 16px;
            }
            
            .content {
                padding: 24px;
            }
            
            .word-group {
                margin-bottom: 40px;
            }
            
            .word-group:first-child {
                margin-top: 0;
            }
            
            .word-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
                padding-bottom: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .word-info {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .word-name {
                font-size: 17px;
                font-weight: 600;
                color: #1a1a1a;
            }
            
            .word-count {
                color: #666;
                font-size: 13px;
                font-weight: 500;
            }
            
            .word-count.hot { color: #dc2626; font-weight: 600; }
            .word-count.warm { color: #ea580c; font-weight: 600; }
            
            .word-index {
                color: #999;
                font-size: 12px;
            }
            
            /* 平台分类容器 */
            .platform-group {
                margin-bottom: 32px;
            }
            
            .platform-title {
                color: #666;
                font-size: 14px;
                font-weight: 600;
                margin: 0 0 16px 0;
                padding: 8px 0;
                border-bottom: 2px solid #e5e7eb;
            }
            
            /* 新闻卡片容器 */
            .news-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 16px;
                margin-bottom: 24px;
            }
            
            /* 新闻卡片样式 */
            .news-card {
                background: #f8f9fa;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 16px;
                transition: all 0.2s ease;
                position: relative;
                overflow: hidden;
            }
            
            .news-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                border-color: #d1d5db;
            }
            
            .news-card.new::before {
                content: "NEW";
                position: absolute;
                top: 12px;
                right: 12px;
                background: #fbbf24;
                color: #92400e;
                font-size: 9px;
                font-weight: 700;
                padding: 3px 6px;
                border-radius: 4px;
                letter-spacing: 0.5px;
            }
            
            .card-header {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 12px;
                flex-wrap: wrap;
            }
            
            .card-source {
                color: #666;
                font-size: 12px;
                font-weight: 500;
            }
            
            .card-rank {
                color: #fff;
                background: #6b7280;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 6px;
                border-radius: 10px;
                min-width: 18px;
                text-align: center;
            }
            
            .card-rank.top { background: #dc2626; }
            .card-rank.high { background: #ea580c; }
            
            .card-time {
                color: #999;
                font-size: 11px;
            }
            
            .card-count {
                color: #059669;
                font-size: 11px;
                font-weight: 500;
            }
            
            .card-title {
                font-size: 15px;
                line-height: 1.4;
                color: #1a1a1a;
                margin: 0 0 8px 0;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .card-link {
                color: #2563eb;
                text-decoration: none;
            }
            
            .card-link:hover {
                text-decoration: underline;
            }
            
            .card-link:visited {
                color: #7c3aed;
            }
            
            /* 传统新闻项样式，保持兼容 */
            .news-item {
                margin-bottom: 20px;
                padding: 16px 0;
                border-bottom: 1px solid #f5f5f5;
                position: relative;
                display: flex;
                gap: 12px;
                align-items: center;
            }
            
            .news-item:last-child {
                border-bottom: none;
            }
            
            .news-item.new::after {
                content: "NEW";
                position: absolute;
                top: 12px;
                right: 0;
                background: #fbbf24;
                color: #92400e;
                font-size: 9px;
                font-weight: 700;
                padding: 3px 6px;
                border-radius: 4px;
                letter-spacing: 0.5px;
            }
            
            .news-number {
                color: #999;
                font-size: 13px;
                font-weight: 600;
                min-width: 20px;
                text-align: center;
                flex-shrink: 0;
                background: #f8f9fa;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                align-self: flex-start;
                margin-top: 8px;
            }
            
            .news-content {
                flex: 1;
                min-width: 0;
                padding-right: 40px;
            }
            
            .news-item.new .news-content {
                padding-right: 50px;
            }
            
            .news-header {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 8px;
                flex-wrap: wrap;
            }
            
            .source-name {
                color: #666;
                font-size: 12px;
                font-weight: 500;
            }
            
            .rank-num {
                color: #fff;
                background: #6b7280;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 6px;
                border-radius: 10px;
                min-width: 18px;
                text-align: center;
            }
            
            .rank-num.top { background: #dc2626; }
            .rank-num.high { background: #ea580c; }
            
            .time-info {
                color: #999;
                font-size: 11px;
            }
            
            .count-info {
                color: #059669;
                font-size: 11px;
                font-weight: 500;
            }
            
            .news-title {
                font-size: 15px;
                line-height: 1.4;
                color: #1a1a1a;
                margin: 0;
            }
            
            .news-link {
                color: #2563eb;
                text-decoration: none;
            }
            
            .news-link:hover {
                text-decoration: underline;
            }
            
            .news-link:visited {
                color: #7c3aed;
            }
            
            .new-section {
                margin-top: 40px;
                padding-top: 24px;
                border-top: 2px solid #f0f0f0;
            }
            
            .new-section-title {
                color: #1a1a1a;
                font-size: 16px;
                font-weight: 600;
                margin: 0 0 20px 0;
            }
            
            .new-source-group {
                margin-bottom: 24px;
            }
            
            .new-source-title {
                color: #666;
                font-size: 13px;
                font-weight: 500;
                margin: 0 0 12px 0;
                padding-bottom: 6px;
                border-bottom: 1px solid #f5f5f5;
            }
            
            .new-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 8px 0;
                border-bottom: 1px solid #f9f9f9;
            }
            
            .new-item:last-child {
                border-bottom: none;
            }
            
            .new-item-number {
                color: #999;
                font-size: 12px;
                font-weight: 600;
                min-width: 18px;
                text-align: center;
                flex-shrink: 0;
                background: #f8f9fa;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .new-item-rank {
                color: #fff;
                background: #6b7280;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 6px;
                border-radius: 8px;
                min-width: 20px;
                text-align: center;
                flex-shrink: 0;
            }
            
            .new-item-rank.top { background: #dc2626; }
            .new-item-rank.high { background: #ea580c; }
            
            .new-item-content {
                flex: 1;
                min-width: 0;
            }
            
            .new-item-title {
                font-size: 14px;
                line-height: 1.4;
                color: #1a1a1a;
                margin: 0;
            }
            
            .error-section {
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 24px;
            }
            
            .error-title {
                color: #dc2626;
                font-size: 14px;
                font-weight: 600;
                margin: 0 0 8px 0;
            }
            
            .error-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            
            .error-item {
                color: #991b1b;
                font-size: 13px;
                padding: 2px 0;
                font-family: 'SF Mono', Consolas, monospace;
            }
            
            .footer {
                margin-top: 32px;
                padding: 20px 24px;
                background: #f8f9fa;
                border-top: 1px solid #e5e7eb;
                text-align: center;
            }
            
            .footer-content {
                font-size: 13px;
                color: #6b7280;
                line-height: 1.6;
            }
            
            .footer-link {
                color: #4f46e5;
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s ease;
            }
            
            .footer-link:hover {
                color: #7c3aed;
                text-decoration: underline;
            }
            
            .project-name {
                font-weight: 600;
                color: #374151;
            }
            
            @media (max-width: 768px) {
                .news-grid {
                    grid-template-columns: 1fr;
                    gap: 12px;
                }
                
                .header-info {
                    grid-template-columns: 1fr 1fr;
                    gap: 12px;
                }
            }
            
            @media (max-width: 480px) {
                body { padding: 12px; }
                .header { padding: 24px 20px; }
                .content { padding: 20px; }
                .footer { padding: 16px 20px; }
                .header-info { grid-template-columns: 1fr; gap: 12px; }
                .save-buttons {
                    position: static;
                    margin-bottom: 16px;
                    display: flex;
                    gap: 8px;
                    justify-content: center;
                    flex-direction: column;
                    width: 100%;
                }
                .save-btn {
                    width: 100%;
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

    # 处理主要统计数据
    if report_data["stats"]:
        total_count = len(report_data["stats"])

        for i, stat in enumerate(report_data["stats"], 1):
            count = stat["count"]

            # 确定热度等级
            if count >= 10:
                count_class = "hot"
            elif count >= 5:
                count_class = "warm"
            else:
                count_class = ""

            escaped_word = html_escape(stat["word"])

            html += f"""
                <div class="word-group">
                    <div class="word-header">
                        <div class="word-info">
                            <div class="word-name">{escaped_word}</div>
                            <div class="word-count {count_class}">{count} 条</div>
                        </div>
                        <div class="word-index">{i}/{total_count}</div>
                    </div>"""

            # 按平台对新闻进行分组
            platform_news = {}
            for title_data in stat["titles"]:
                source_name = title_data["source_name"]
                if source_name not in platform_news:
                    platform_news[source_name] = []
                platform_news[source_name].append(title_data)
            
            # 遍历每个平台，展示该平台下的新闻卡片
            for platform, titles in platform_news.items():
                html += f"""
                    <div class="platform-group">
                        <div class="platform-title">{html_escape(platform)} · {len(titles)}条</div>
                        <div class="news-grid">"""
                
                # 为每个平台下的新闻创建卡片
                for title_data in titles:
                    is_new = title_data.get("is_new", False)
                    new_class = "new" if is_new else ""
                    
                    html += f"""
                        <div class="news-card {new_class}">
                            <div class="card-header">
                                <span class="card-source">{html_escape(title_data["source_name"])}</span>"""
                    
                    # 处理排名显示
                    ranks = title_data.get("ranks", [])
                    if ranks:
                        min_rank = min(ranks)
                        max_rank = max(ranks)
                        rank_threshold = title_data.get("rank_threshold", 10)
                    
                        # 确定排名等级
                        if min_rank <= 3:
                            rank_class = "top"
                        elif min_rank <= rank_threshold:
                            rank_class = "high"
                        else:
                            rank_class = ""
                    
                        if min_rank == max_rank:
                            rank_text = str(min_rank)
                        else:
                            rank_text = f"{min_rank}-{max_rank}"
                    
                        html += f'<span class="card-rank {rank_class}">{rank_text}</span>'
                    
                    # 处理时间显示
                    time_display = title_data.get("time_display", "")
                    if time_display:
                        # 简化时间显示格式，将波浪线替换为~
                        simplified_time = (
                            time_display.replace(" ~ ", "~")
                            .replace("[", "")
                            .replace("]", "")
                        )
                        html += (
                            f'<span class="card-time">{html_escape(simplified_time)}</span>'
                        )
                    
                    # 处理出现次数
                    count_info = title_data.get("count", 1)
                    if count_info > 1:
                        html += f'<span class="card-count">{count_info}次</span>'
                    
                    html += """
                            </div>
                            <div class="card-title">"""
                    
                    # 处理标题和链接
                    escaped_title = html_escape(title_data["title"])
                    link_url = title_data.get("mobile_url") or title_data.get("url", "")
                    
                    if link_url:
                        escaped_url = html_escape(link_url)
                        html += f'<a href="{escaped_url}" target="_blank" class="card-link">{escaped_title}</a>'
                    else:
                        html += escaped_title
                    
                    html += """
                            </div>
                        </div>"""
                
                html += """
                    </div>
                </div>"""

            html += """
                </div>"""

    # 处理新增新闻区域
    if report_data["new_titles"]:
        html += f"""
                <div class="new-section">
                    <div class="new-section-title">本次新增热点 (共 {report_data['total_new_count']} 条)</div>"""

        for source_data in report_data["new_titles"]:
            escaped_source = html_escape(source_data["source_name"])
            titles_count = len(source_data["titles"])

            html += f"""
                    <div class="new-source-group">
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
                    html += f'<a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
                else:
                    html += escaped_title

                html += """
                                </div>
                            </div>
                        </div>"""

            html += """
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
