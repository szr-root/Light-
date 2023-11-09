"""
v1版本
    在视图函数：
        def customer_list(request):
            # 所有数据
            queryset = models.Customer.objects.filter(active=1).select_related('level')

            pager = Pagination(request, queryset)
            context = {
                "queryset": queryset[pager.start:pager.end],
                "pager_string": obj.html()
            }
            return render(request, 'customer_list.html', context)

    在页面上：
        {% for row in queryset %}
            {{row.id}}
        {% endfor %}

        <ul class="pagination">
            {{ pager_string }}
        </ul>

v2版本
    在视图函数：
        def customer_list(request):
            # 所有数据
            queryset = models.Customer.objects.filter(active=1).select_related('level')

            pager = Pagination(request, queryset)
            return render(request, 'customer_list.html', {"pager":pager})

    在页面上：
        {% for row in pager.queryset %}
            {{row.id}}
        {% endfor %}

        <ul class="pagination">
            {{ pager.html }}
        </ul>

"""
import copy
from django.utils.safestring import mark_safe


class Pagination(object):
    """ 分页 """

    def __init__(self, request, query_set, per_page_count=10):
        self.query_dict = copy.deepcopy(request.GET)
        self.query_dict._mutable = True

        self.query_set = query_set
        total_count = query_set.count()
        self.total_count = total_count

        # 计算出总共有多少页面
        self.total_page, div = divmod(total_count, per_page_count)
        if div:
            self.total_page += 1

        # 字符串格式  123908sdfsdf
        page = request.GET.get('page', "1")
        if not page.isdecimal():
            page = 1
        else:
            page = int(page)
            if page <= 0:
                page = 1
            if page > self.total_page:
                page = self.total_page

        self.page = page
        self.per_page_count = per_page_count

        self.start = (page - 1) * per_page_count
        self.end = page * per_page_count

    def html(self):
        pager_list = []
        if not self.total_page:
            return ""

        # 总页码小于11
        if self.total_page <= 11:
            start_page = 1
            end_page = self.total_page
        else:
            # 总页码比较多
            # 判断当前页 <=6: 1~11
            if self.page <= 6:
                start_page = 1
                end_page = 11
            else:
                if (self.page + 5) > self.total_page:
                    start_page = self.total_page - 10
                    end_page = self.total_page
                else:
                    start_page = self.page - 5
                    end_page = self.page + 5

        pager_list.append('<ul class="pagination">')

        self.query_dict.setlist('page', [1])
        pager_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        if self.page > 1:
            self.query_dict.setlist('page', [self.page - 1])
            pager_list.append('<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode()))

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist('page', [i])
            if i == self.page:
                item = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                item = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            pager_list.append(item)

        if self.page < self.total_page:
            self.query_dict.setlist('page', [self.page + 1])
            pager_list.append('<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode()))

        self.query_dict.setlist('page', [self.total_page])
        pager_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        pager_list.append('<li class="disabled"><a>数据{}条{}页</a></li>'.format(self.total_count, self.total_page))
        pager_string = mark_safe("".join(pager_list))

        pager_list.append('</ul>')

        return pager_string

    def queryset(self):
        if self.total_count:
            return self.query_set[self.start:self.end]
        return self.query_set
