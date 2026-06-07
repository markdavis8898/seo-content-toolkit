#!/usr/bin/env python3
"""
SEO Article Generator — Generate structured, SEO-optimized content for trade documentation topics.
"""

import argparse
import json
import random
from datetime import datetime


# Template sections for trade documentation articles
TEMPLATES = {
    'process_guide': {
        'title_pattern': [
            "{service}办理流程完整指南",
            "{service}申请流程及注意事项",
            "如何办理{service}？完整流程解析",
        ],
        'sections': [
            "什么是{service}",
            "办理{service}需要哪些材料",
            "{service}办理流程详解",
            "常见问题解答",
            "办理周期与费用",
        ],
    },
    'comparison': {
        'title_pattern': [
            "{service1}与{service2}的区别",
            "{service1}还是{service2}？如何选择",
            "{service1}vs{service2}对比分析",
        ],
        'sections': [
            "什么是{service1}",
            "什么是{service2}",
            "主要区别对比",
            "适用场景分析",
            "选择建议",
        ],
    },
}


SERVICES = [
    "原产地证", "CO证书", "FORM A", "FORM E", "FORM F",
    "海牙认证", "使馆认证", "商事证明书", "贸促会认证",
    "自由销售证书", "出口商检", "报关单证",
]

EN_SERVICES = [
    "Certificate of Origin",
    "Apostille",
    "使馆认证 (Embassy Legalization)",
    "CCPIT Certification",
    "Free Sale Certificate",
    "Form A (GSP)",
    "Form E (ASEAN-China FTA)",
    "Form F (China-Chile FTA)",
    "Health Certificate",
    "Phytosanitary Certificate",
]


def generate_article(template_type, service_vars, language='zh'):
    """Generate a structured article based on template."""
    template = TEMPLATES.get(template_type, TEMPLATES['process_guide'])
    
    # Select title
    title_pattern = random.choice(template['title_pattern'])
    title = title_pattern.format(**service_vars)
    
    # Generate content sections
    content_parts = [f"# {title}", ""]
    
    for section in template['sections']:
        section_title = section.format(**service_vars)
        content_parts.append(f"## {section_title}")
        content_parts.append("")
        content_parts.append(
            f"本文详细介绍{service_vars.get('service', '相关服务')}的办理流程、"
            f"所需材料和注意事项，帮助您快速完成单证办理。"
        )
        content_parts.append("")
    
    return {
        'title': title,
        'content': '\n'.join(content_parts),
        'meta_description': f"专业{title}办理指南，包括流程、材料、费用及注意事项。",
        'language': language,
        'generated_at': datetime.utcnow().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(
        description='Generate SEO-optimized trade documentation articles'
    )
    parser.add_argument('--template', '-t', default='process_guide',
                       choices=TEMPLATES.keys(),
                       help='Article template type')
    parser.add_argument('--service', '-s', default='原产地证',
                       help='Primary service/topic')
    parser.add_argument('--language', '-l', default='zh',
                       choices=['zh', 'en'],
                       help='Article language')
    parser.add_argument('--count', '-c', type=int, default=1,
                       help='Number of articles to generate')
    parser.add_argument('--output', '-o', default='articles.json',
                       help='Output file path')
    
    args = parser.parse_args()
    
    articles = []
    for i in range(args.count):
        if args.language == 'en':
            service = random.choice(EN_SERVICES)
        else:
            service = random.choice(SERVICES)
        
        article = generate_article(
            args.template,
            {'service': service, 'service1': service, 'service2': random.choice(SERVICES)},
            args.language
        )
        articles.append(article)
        print(f"  ✅ Generated: {article['title']}")
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ {len(articles)} articles saved to {args.output}")


if __name__ == '__main__':
    main()
