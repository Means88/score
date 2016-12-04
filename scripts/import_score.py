# coding=utf-8
from score.models import Album, Score

import re
import os


def _import_from_html(content):
    score = {}
    m = re.search(r'<h1 id="-">([^<]*)</h1>', content)
    score['title'] = m.group(1) if m else ""

    m = re.search(r'<img src="([^"]*)"[^>]*>', content)
    score['cover'] = m.group(1) if m else ""

    m = re.search(r'<li>专辑：<span class="inline-block highlight">([^<]*)</span></li>', content)
    score['album'] = m.group(1) if m else ""

    m = re.search(r'<li>作词：<span class="inline-block highlight">([^<]*)</span></li>', content)
    score['lyricist'] = m.group(1) if m else ""

    m = re.search(r'<li>作曲：<span class="inline-block highlight">([^<]*)</span></li>', content)
    score['composer'] = m.group(1) if m else ""

    m = re.search(r'<li>编曲：<span class="inline-block highlight">([^<]*)</span></li>', content)
    score['arranger'] = m.group(1) if m else ""

    m = re.search(r'<li>歌手：<span class="inline-block highlight">([^<]*)</span></li>', content)
    score['artist'] = m.group(1) if m else ""

    m = re.search(r'>@ ([^<]*) <', content)
    score['by'] = m.group(1) if m else ""

    m = re.search(r'<pre class="editor-colors lang-text">([^`]*)</pre>', content)
    score['content'] = m.group(1) if m else ""

    return score


def _import_from_md(content):
    score = {}
    lines = content.split('\n')
    try:
        if lines[0][:2] != "# ":
            print "The first line is:\n%s\nskip" % lines[0]
            return None
    except:
        return None
    score['title'] = lines[0][2:]

    m = re.search(r'!\[[^\]]*\]\(([^\)]*)\)', lines[1])
    score['cover'] = m.group(1) if m else ""

    m = re.search(r'专辑：[^>]*>([^<]*)</span>', content)
    score['album'] = m.group(1) if m else ""

    m = re.search(r'作词：[^>]*>([^<]*)</span>', content)
    score['lyricist'] = m.group(1) if m else ""

    m = re.search(r'作曲：[^>]*>([^<]*)</span>', content)
    score['composer'] = m.group(1) if m else ""

    m = re.search(r'编曲：[^>]*>([^<]*)</span>', content)
    score['arranger'] = m.group(1) if m else ""

    m = re.search(r'歌手：[^>]*>([^<]*)</span>', content)
    score['artist'] = m.group(1) if m else ""

    m = re.search(r'>@ ([^<]*)<', content)
    score['by'] = m.group(1) if m else ""

    m = re.search(r"```([^`]*)```", content)
    score['content'] = m.group(1) if m else ""

    return score


def _save_score(score):
    print 'saving...'
    for k in score:
        score[k] = score[k].strip()

    print 'finding...'
    if Score.objects.filter(title=score['title']).exists():
        print 'The score %s has already exist, skip' % score['title']
        return None

    print 'finding album...'
    album, create = Album.objects.get_or_create(title=score['album'])
    print 'creating...'
    return Score.objects.create(title=score['title'],
                                cover=score['cover'],
                                album=album,
                                artist=score['artist'],
                                lyricist=score['lyricist'],
                                composer=score['composer'],
                                arranger=score['arranger'],
                                by=score['by'],
                                content=score['content']
                                )


def run(*args):
    exist_count = 0
    not_valid_count = 0
    created_count = 0
    for rootdir in args:
        print rootdir
        for parent, dirnames, filenames in os.walk(rootdir):
            path = parent.split(os.sep)[::-1]
            while path.pop() != 'MusicScore':
                pass
            for filename in filenames:
                print ''
                print filename
                ext = os.path.splitext(filename)[1]
                if ext != '.md' and ext != '.html':
                    print 'skip %s' % filename
                    continue
                fp = open(os.sep.join((parent, filename)))
                content = fp.read()
                print 'import...'
                if ext == '.md':
                    score = _import_from_md(content)
                else:
                    score = _import_from_html(content)

                if not score:
                    print '%s is not a valid score' % filename
                    not_valid_count += 1
                    continue

                score = _save_score(score)
                if not score:
                    exist_count += 1
                    continue

                created_count += 1
                tags = score.tags
                for tag in path:
                    tags.append(tag)
                score.tags = tags
                score.save()

    print 'finished. %s existed, %s not valid, %s created. Total %s' \
          % (exist_count, not_valid_count, created_count, exist_count + not_valid_count + created_count)
