# The project is temporarily suspended!

## VietNam Social Scraper
Dự án thu thập dữ liệu tiếng Việt từ các mạng xã hội, bao gồm:
- [x] Facebook
- [x] Instagram
- [x] Youtube
- [x] Forum
- [x] Xem dự án thu thập [Các đầu báo online](https://github.com/nguyenvanhieuvn/news-crawler)

> Dự án phục vụ cho mục đích công việc & học tập của cá nhân. 
### Youtube 
- Thu thập các **bình luận tiếng việt** bên dưới video youtube. 
- Source code nằm bên trong thư mục [youtube](/youtube)

Trong module này, mình có sử dụng một dự án bên thứ 3 [tại đây](https://github.com/egbertbouman/youtube-comment-downloader) để download comment của một video youtube.
Tích hợp với chức năng tự động tìm kiếm các video mới (không trùng lặp).

Trên thực tế, mình đã chạy 3 ngày và tập URL hàng đợi vẫn đang tăng dần đều.

Cập nhật chức năng:

- [x] Cấu hình động
- [x] Hỗ trợ proxy
- [x] Chạy đa luồng
- [x] Lọc video tiếng Việt theo title
- [x] Khởi tạo list url ban đầu (lấy text gần domain chúng ta cần)
Cách chạy:
```text
$ cd youtube
$ python app.py 
```

Minh họa dữ liệu thu thập:
```text
{"cid": "UgyYrx8P6lVED3YzMuR4AaABAg", "text": "[15ffff]0:33 để ýcu của cu tượng nha", "time": "9 tháng trước", "author": "SWAT• BéGấu", "votes": "2", "photo": "https://yt3.ggpht.com/a/AGF-l7-e9aTlCO7D7OLG6ZpXhNjeKkUq_lmRvGY4vg=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgxaQkc5QkvC2yKstpd4AaABAg", "text": ":))) không phải vậy đâu bác ơi :)))", "time": "10 tháng trước", "author": "GURU TV", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l79Onlg7YYUOUfX_Q4_TK1QKlMZgD1i4jheRaQ=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "Ugxsx8RRVeVZi-R-TBh4AaABAg", "text": "Anh o anh tho thach 24h", "time": "10 tháng trước", "author": "Vanthanh Truong", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l7-5qrSPNxw4yIGC96jI3xCVNhjasjL2lmNJhA=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "Ugz5N8gjlDLJC8Fz6St4AaABAg", "text": "4/2019 thích anh Nam giải mã ảo thuật kiểu như này ☺️☺️", "time": "10 tháng trước", "author": "Giang Sagittarius", "votes": "37", "photo": "https://yt3.ggpht.com/a/AGF-l7_jl9lo2LMjCD5_w9-IJWZcDfS5HA3RMJce6g=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "Ugw3QWtiz6qnbELcvZB4AaABAg", "text": "Áo thuật sửa rồi", "time": "11 tháng trước", "author": "lý hoàng dinh", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l78ULgZL7QT2DbuBEnN7Njma-6PucZRU_JrnQA=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgwxVd_v0vncJi8ukjh4AaABAg", "text": "Ai nhớ thượng gà k", "time": "11 tháng trước", "author": "Văn Việt", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l7-I_QmuUZmp0VszF47dLYy4dqSeCweYEPP1Yw=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgzlqjNU03VVcne9nUV4AaABAg", "text": "anh nam thông minh quá. ai còn xem tập này điểm danh nào", "time": "11 tháng trước", "author": "LXS Vlog", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l7_13MYu2_mAMkNsNObwT62cah23pOqh4qI3Pg=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgxmXT8nzgJi26TbK2d4AaABAg", "text": "Như thế  thì ai cũng  làm được", "time": "11 tháng trước", "author": "Cáng Chương", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l7_sCbuafD5UvOw4RnJRbLmFL3TQ4wn6qfKBkA=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgzST_8oqNLMQGtVEPt4AaABAg", "text": "Thằng gà 0:32 để ý nhé 😂😂😂😂", "time": "1 năm trước", "author": "Quang Thanh", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l79iQbgNswGEQ18orF68_sK3f4CUSy5QuQ=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgyhNdzeTw_kM4b2GjF4AaABAg", "text": "2019 ai còn xem", "time": "1 năm trước", "author": "Lụa Hồng", "votes": "2", "photo": "https://yt3.ggpht.com/a/AGF-l78UKWiwtj1RWjAcgCkGWFJhy0JUAnmdQskFbg=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "Ugz4xGXEgZ0DNE2NOoV4AaABAg", "text": "nhung ma co gai nguc to lam a oi dam la xước het nguoc", "time": "1 năm trước", "author": "vn hvt", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l7_r5Qu45x1wZZZl6RlpK7T6yTWyejKcW2W6DQ=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "Ugyg7XKy78VwWX1EsqZ4AaABAg", "text": "Chẵng có gì hay cả", "time": "1 năm trước", "author": "Hoàng Duyên Phan Thị", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l78rGjehLz9Cr4zQVk9tiUb5pQuqvj8ONgJJ7Q=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "Ugz-td0Bv9M0xZXy-0B4AaABAg", "text": "2019 con ai xem hong", "time": "1 năm trước", "author": "Cuong Huynh", "votes": "3", "photo": "https://yt3.ggpht.com/a/AGF-l78yqXkE_W9JuraO8-yXqmscMt5HiTvTosbcSA=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgwWpTRlDJs8WY32lr14AaABAg", "text": "Đây là anh Nam đang quay Like giảiiiiiiiiii trí", "time": "1 năm trước", "author": "Hie Nguyen", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l79flXTH-jUPYVD9pIEh26WVA9L2X2aiYzBxng=s48-c-k-c0xffffffff-no-rj-mo"}
{"cid": "UgysLxAaKhiP5gObEJZ4AaABAg", "text": "Hay 👏👏👏💋😸😸😝", "time": "1 năm trước", "author": "Tuan Mr", "votes": "1", "photo": "https://yt3.ggpht.com/a/AGF-l78uW1yPa36LwXFb2HB2g4JePdDbDVGNZA6SqA=s48-c-kfffff-no-rj-mo"}

``` 

### Instagram
- Trong phần code [instagram](instagram) chỉ có module tìm ra các tài khoản được xác minh qua từ khóa.
- Từ khóa mình sử dụng là tên người nổi tiếng tại Việt Nam
- Chức năng thu thập comment sử dụng mã nguồn Java khác [ở đây](https://github.com/postaddictme/instagram-java-scraper)

Vì lý do comment trên Instagram khá ít, nhiều quảng cáo nên mình không tập trung phát triển cái này.

## Facebook
- Thu thập bài viết, comment từ các facebook page.
- Hỗ trợ facebook với cài đặt ngôn ngữ là tiếng Anh (Chưa kiểm tra với ngôn ngữ khác).
- Tốc độ chậm do tránh facebook khóa tài khoản.
- Hỗ trợ cấu hình động
- Trình tự: -> Thu thập tất cả bài viết trên 1 page -> Thu thập tất cả comment trên một bài viết.
- Chưa đăng nhập được trên server (do bị dính checkpoint), fb báo vị trí đăng nhập lạ
### Cách chạy:
- Cài đặt Selenium và Firefox web driver cho Python
- Cài virtual display (tùy chọn, cho OS server)
```text
$ cd facebook 
# Thu thập bài viết (post url, post_id)
$ python page_scraper -u username -p password -i page_id -o output.jl
# Thu thập comment từ bài viết
python post_scraper -u username -p password -i post_url -o output.jl
``` 

Minh họa dữ liệu thu thập:
```text
# Dữ liệu bài viết
{"post_id": "2916688705092172", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916688705092172&id=871029179658145", "post_date": "February 23 at 9:19 PM"}
{"post_id": "2916578875103155", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916578875103155&id=871029179658145", "post_date": "February 23 at 8:31 PM"}
{"post_id": "2916509915110051", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916509915110051&id=871029179658145", "post_date": "February 23 at 8:03 PM"}
{"post_id": "2916419771785732", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916419771785732&id=871029179658145", "post_date": "February 23 at 7:15 PM"}
{"post_id": "2916385668455809", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916385668455809&id=871029179658145", "post_date": "February 23 at 6:56 PM"}
{"post_id": "2916259285135114", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916259285135114&id=871029179658145", "post_date": "February 23 at 5:48 PM"}
{"post_id": "2916174625143580", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916174625143580&id=871029179658145", "post_date": "February 23 at 5:00 PM"}
{"post_id": "2916167478477628", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916167478477628&id=871029179658145", "post_date": "February 23 at 4:56 PM"}
{"post_id": "2916096941818015", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2916096941818015&id=871029179658145", "post_date": "February 23 at 4:14 PM"}
{"post_id": "2915958645165178", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2915958645165178&id=871029179658145", "post_date": "February 23 at 2:33 PM"}
{"post_id": "2915889441838765", "post_url": "https://mbasic.facebook.com/story.php?story_fbid=2915889441838765&id=871029179658145", "post_date": "February 23 at 1:41 PM"}

# Dữ liệu comment
{"author": "Nguyễn Thị Minh Anh", "author_url": "https://mbasic.facebook.com/Manhhhh.10?rc=p&refid=52&__tn__=R", "text": "Dcm đéo còn từ gì để diễn tả luôn =)) khổ chị gái vl =))", "reply_to": "ROOT"}
{"author": "Trương Minh Khôi", "author_url": "https://mbasic.facebook.com/TRUONGMINHKHOI2008?rc=p&__tn__=R", "text": "Vũ Huyền Trangg có lý :3", "reply_to": "Vũ Huyền Trangg"}
{"author": "Huế Mello", "author_url": "https://mbasic.facebook.com/mello.hue?rc=p&__tn__=R", "text": "Chuẩn đét b êii", "reply_to": "Vũ Huyền Trangg"}
{"author": "Vũ Huyền Trangg", "author_url": "https://mbasic.facebook.com/profile.php?id=100008458657965&rc=p&__tn__=R", "text": "Huế Mello", "reply_to": "Vũ Huyền Trangg"}
{"author": "Vũ Danh Hùng", "author_url": "https://mbasic.facebook.com/hungshidro?rc=p&__tn__=R", "text": "kiểu này là bàn phím bị kẹt này =))", "reply_to": "Vũ Huyền Trangg"}
{"author": "Vũ Huyền Trangg", "author_url": "https://mbasic.facebook.com/profile.php?id=100008458657965&rc=p&__tn__=R", "text": "Vũ Danh Hùng ??", "reply_to": "Vũ Huyền Trangg"}
{"author": "Nguyễn Phương Lam", "author_url": "https://mbasic.facebook.com/lamtung.skymtp.5794622k?rc=p&refid=52&__tn__=R", "text": "rình nhà nó ở đâu đem sơn đến phun đầy ô tô cho đỡ tức :3", "reply_to": "ROOT"}
{"author": "Thẩm Tiếu Đình", "author_url": "https://mbasic.facebook.com/profile.php?id=100045383620041&rc=p&refid=52&__tn__=R", "text": "", "reply_to": "ROOT"}
{"author": "Nguyễn Thảo Nguyên", "author_url": "https://mbasic.facebook.com/thaonguyen.1210.2003?rc=p&refid=52&__tn__=R", "text": "không nói nhiều... 🙂", "reply_to": "ROOT"}
{"author": "Hà Hương", "author_url": "https://mbasic.facebook.com/thalia.hero.9?rc=p&refid=52&__tn__=R", "text": "Anh nyc chắc là súc vật thành tinh phỏng??", "reply_to": "ROOT"}
{"author": "Nguyễn Thu Huyền", "author_url": "https://mbasic.facebook.com/NTH130401?rc=p&refid=52&__tn__=R", "text": "Lòng chung thủy của đàn bà được thử thách khi người đàn ông không có gì trong tay, còn lòng chung thủy của đàn ông được thử thách khi anh ta có đầy đủ :)))", "reply_to": "ROOT"}
{"author": "Dương Nguyễn", "author_url": "https://mbasic.facebook.com/boson.chaucon?rc=p&refid=52&__tn__=R", "text": "Loại này có cho chúng tôi còn đánh thêm", "reply_to": "ROOT"}
{"author": "Trần Quang Anh", "author_url": "https://mbasic.facebook.com/Quanganhsociu69?rc=p&refid=52&__tn__=R", "text": "Sao đéo húc nó một phát hay xin nhẹ một bên gương cho bõ ghét.quá non", "reply_to": "ROOT"}
{"author": "Hằng Apple", "author_url": "https://mbasic.facebook.com/apple.hang.1004?rc=p&refid=52&__tn__=R", "text": "Tội chị gái", "reply_to": "ROOT"}
```
