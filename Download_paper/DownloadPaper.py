import os
import requests
from bs4 import BeautifulSoup
import re
import arxiv

# 创建一个文件夹来保存下载的文章
if not os.path.exists('CVPR2024'):
    os.makedirs('CVPR2024')

if not os.path.exists('AAAI2024'):
    os.makedirs('AAAI2024')

def get_paper_title(arxiv_id):
    try:
        paper_info = arxiv.query(id_list=[arxiv_id])[0]
        title = paper_info['title']
        return title
    except Exception as e:
        print("Error:", e)
        return None
def search_and_download(author_name,file_name):
    # 构建搜索作者的 URL

    result = re.split(r'[ :\s]', author_name)
    result = '+'.join(result)
    search_url = f'https://arxiv.org/search/?query={result}&searchtype=all&source=header'
    # 发送 HTTP 请求获取搜索结果页面内容
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到所有搜索结果的论文链接
        paper_links = soup.find_all('p', class_='list-title is-inline-block')
        if paper_links:
            for link in paper_links:
                try:
                    # 获取论文标题和链接
                    title = link.text.strip()
                    pdf_abs = link.find('a')['href']
                    pdf_ID = re.split(r'[/]', pdf_abs)[-1]
                    pdf_link =  'https://arxiv.org/pdf/{}.pdf'.format(pdf_ID)

                    search = arxiv.Search(
                        id_list=[pdf_ID],
                    )
                    for result in search.results():
                        title= result.title

                    save_filepath=f'{file_name}/{title}.pdf'
                    save_filepath = save_filepath.replace(':', '')
                    download_large_pdf(pdf_link,save_filepath)
                except Exception as e:
                    print(f"An error occurred: {e}")
        else:
            print(f"No papers found for '{author_name}'.")
    else:
        print("Failed to retrieve search results.")


def download_large_pdf(url, filename, chunk_size=1024):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        print("PDF 下载成功 {} ！".format(filename))
    except Exception as e:
        print("PDF 下载失败 {}".format(filename), e)

if __name__ == "__main__":
    CVPR_2024_paper_list = [
                            # 'Source-Free Domain Adaptation with Frozen Multimodal Foundation Model',
                            # 'Boosting Object Detection with Zero-Shot Day-Night Domain Adaptation',
                            # 'LEAD: Learning Decomposition for Source-free Universal Domain Adaptation',
                            # 'Unsupervised Video Domain Adaptation with Masked Pre-Training and Collaborative Self-Training',
                            # 'Domain-Agnostic Mutual Prompting for Unsupervised Domain Adaptation',
                            # 'Split to Merge: Unifying Separated Modalities for Unsupervised Domain Adaptation',

                  'Density-guided Translator Boosts Synthetic-to-Real Unsupervised Domain Adaptive Segmentation of 3D Point Clouds',
                  'Pseudo Label Refinery for Unsupervised Domain Adaptation on Cross-dataset 3D Object Detection',
                  'Learning CNN on ViT: A Hybrid Model to Explicitly Class-specific Boundaries for Domain Adaptation',
                  'Active Domain Adaptation with False Negative Prediction for Object Detection',
                  # 'Open Set Domain Adaptation for Semantic Segmentation',
                  'Parameter Efficient Self-Supervised Geospatial Domain Adaptation',
                  'Stable Neighbor Denoising for Source-free Domain Adaptive Segmentation',
                  # 'Unified Language-driven Zero-shot Domain Adaptation',
                  'Capture Now and Embrace Future: A Versatile Framework for Continual Test-Time Domain Adaptation',
                  'UniMix: Towards Domain Adaptive and Generalizable LiDAR Semantic Segmentation in Adverse Weather',
                  # 'Universal Semi-Supervised Domain Adaptation by Mitigating Common-Class Bias',
                  'Discriminative Pattern Calibration Mechanism for Source-Free Domain Adaptation',
                  'Construct to Associate: Cooperative Context Learning for Domain Adaptive Point Cloud Segmentation',
                  'Understanding and Improving Source-free Domain Adaptation from a Theoretical Perspective',
                  'CAT: Exploiting Inter-Class Dynamics for Domain Adaptive Object Detection',
                  'Unveiling the Unknown: Unleashing the Power of Unknown to Known in Open-Set Source-Free Domain Adaptation'
    ]

    AAAI_2024_paper_list = ['On Unsupervised Domain Adaptation: Pseudo Label Guided Mixup for Adversarial Prompt Tuning',
                            'Probability-Polarized Optimal Transport for Unsupervised Domain Adaptation',
                            'Pay Attention to Target: Relation-Aware Temporal Consistency for Domain Adaptive Video Semantic Segmentation',
                            # 'Confusing Pair Correction Based on Category Prototype for Domain Adaptation under Noisy Environments',
                            'Low Category Uncertainty and High Training Potential Instance Learning for Unsupervised Domain Adaptation']


    for paper_name in AAAI_2024_paper_list:
        file_name = 'AAAI2024'
        search_and_download(paper_name,file_name)

    for paper_name in CVPR_2024_paper_list:
        file_name = 'CVPR2024'
        search_and_download(paper_name,file_name)