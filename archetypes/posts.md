---
title: "{{ replace .File.ContentBaseName "-" " " | strings.FirstUpper }}"
slug: {{ .File.ContentBaseName }}
description: ""
tags: []
date: {{ .Date }}
draft: true
---

# {{ replace .File.ContentBaseName "-" " " | strings.FirstUpper }}
