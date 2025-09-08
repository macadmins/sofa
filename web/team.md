---
title: Team
layout: doc
---

<script setup>
import { VPTeamMembers } from 'vitepress/theme'

const coreMembers = [
  { 
    avatar: 'https://github.com/arubdesu.png',
    name: 'Allister Banks', 
    title: 'Core Contributor', 
    links: [{ icon: 'github', link: 'http://github.com/arubdesu' }] 
  },
    { 
    avatar: 'https://github.com/headmin.png',
    name: 'Henry Stamerjohann', 
    title: 'Core Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/headmin' }] 
  },
   { 
    avatar: 'https://github.com/grahampugh.png',
    name: 'Graham Pugh', 
    title: 'Core Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/grahampugh' }] 
  },
  { 
    avatar: 'https://github.com/grahamgilbert.png',
    name: 'Graham Gilbert', 
    title: 'Core Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/grahamgilbert' }] 
  },

    { 
    avatar: 'https://github.com/erikng.png',
    name: 'Erik Gomez', 
    title: 'Core Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/erikng' }] 
  },
  { 
    avatar: 'https://github.com/natewalck.png',
    name: 'Nate Walck', 
    title: 'Core Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/natewalck' }] 
  },
  { 
    avatar: 'https://github.com/johnnyramos.png',
    name: 'Johnny Ramos', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/johnnyramos' }] 
  },
  { 
    avatar: 'https://github.com/keeleysam.png',
    name: 'Samuel Keeley', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/keeleysam' }] 
  }
]

const communityMembers = [
    { 
    avatar: 'https://github.com/homebysix.png',
    name: 'Elliot Jordan', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/homebysix' }] 
  },
  { 
    avatar: 'https://github.com/jp-cpe.png',
    name: 'Jonathan Porter', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/jp-cpe' }] 
  },
    { 
    avatar: 'https://github.com/aschwanb.png',
    name: 'Balz Aschwanden', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/aschwanb' }] 
  },
  { 
    avatar: 'https://github.com/lashomb.png',
    name: 'Brian LaShomb', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/lashomb' }] 
  },
  { 
    avatar: 'https://github.com/seanchristians.png',
    name: 'Sean Christians', 
    title: 'Community Contributor', 
    links: [{ icon: 'github', link: 'https://github.com/seanchristians' }] 
  }
]
</script>


# MacAdmins Open Source + SOFA ❤️ community

This is a list of early contributors to SOFA. 

## Core contributors
<VPTeamMembers size="small" :members="coreMembers" />

## Community contributors
<VPTeamMembers size="small" :members="communityMembers" />
