import re

# 패턴 컴파일
pattern = re.compile(r'\bfoo\b')

# 검색할 문자열
text = "bar foo baz"

# match 사용 예
match = pattern.match(text)
print('match:', match)  # 문자열 시작부터 검색하므로 None 반환

# search 사용 예
search = pattern.search(text)
print('search:', search.group())  # 'foo' 반환

# findall 사용 예
findall = pattern.findall(text)
print('findall:', findall)  # ['foo'] 반환

# sub 사용 예
sub = pattern.sub('qux', text)
print('sub:', sub)  # 'bar qux baz' 반환