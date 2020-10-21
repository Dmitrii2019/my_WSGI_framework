from controller import main_view, create_category_view, create_course_view,\
    category_list, contact_view, course_list, copy_course

urls = {
    '/': main_view,
    '/create-category/': create_category_view,
    '/create-course/': create_course_view,
    '/contact/': contact_view,
    '/category-list/': category_list,
    '/course-list/': course_list,
    '/copy-course/': copy_course,
}
