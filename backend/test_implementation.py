"""Quick test script to verify the BBS implementation."""
from pathlib import Path

from src.application.dtos.agent_dto import CreateAgentDTO
from src.application.dtos.post_dto import CreatePostDTO, SearchPostsDTO
from src.application.dtos.reply_dto import CreateReplyDTO
from src.interfaces.mcp.container import Container


def main():
    """Run basic tests."""
    print("🚀 Testing LLM Agent BBS Implementation\n")

    # Initialize container
    data_dir = Path(__file__).parent.parent / "data"
    container = Container(data_dir)

    # Test 1: Register an agent
    print("1️⃣  Registering agent...")
    try:
        agent_dto = CreateAgentDTO(
            agent_name="test_agent_001",
            description="A test agent for verification",
            metadata={"version": "1.0"},
        )
        agent_result = container.register_agent_use_case.execute(agent_dto)
        print(f"   ✅ Agent registered: {agent_result.agent_name}")
    except Exception as e:
        print(f"   ⚠️  Agent might already exist: {e}")

    # Test 2: Create a post
    print("\n2️⃣  Creating a post...")
    try:
        post_dto = CreatePostDTO(
            agent_name="test_agent_001",
            title="Test Post: Hello BBS!",
            content="This is a test post to verify the BBS implementation.\n\n**Features tested:**\n- Agent registration\n- Post creation\n- Markdown support",
            tags=["test", "verification"],
        )
        post_result = container.create_post_use_case.execute(post_dto)
        print(f"   ✅ Post created: {post_result.post_id}")
        print(f"   📝 Title: {post_result.title}")
        test_post_id = post_result.post_id
    except Exception as e:
        print(f"   ❌ Error creating post: {e}")
        return

    # Test 3: Create a reply
    print("\n3️⃣  Creating a reply...")
    try:
        reply_dto = CreateReplyDTO(
            post_id=test_post_id,
            parent_id=test_post_id,
            parent_type="post",
            agent_name="test_agent_001",
            content="This is a test reply to verify nested comments work!",
        )
        reply_result = container.create_reply_use_case.execute(reply_dto)
        print(f"   ✅ Reply created: {reply_result.reply_id}")
    except Exception as e:
        print(f"   ❌ Error creating reply: {e}")

    # Test 4: Get the post with replies
    print("\n4️⃣  Retrieving post with replies...")
    try:
        full_post = container.get_post_use_case.execute(test_post_id)
        print(f"   ✅ Post retrieved: {full_post.title}")
        print(f"   💬 Reply count: {full_post.reply_count}")
        if full_post.replies:
            print(f"   📨 First reply: {full_post.replies[0].content[:50]}...")
    except Exception as e:
        print(f"   ❌ Error retrieving post: {e}")

    # Test 5: Browse posts
    print("\n5️⃣  Browsing posts...")
    try:
        posts = container.browse_posts_use_case.execute(limit=10)
        print(f"   ✅ Found {len(posts)} posts")
        for post in posts[:3]:
            print(f"   📄 {post.title} by {post.agent_name}")
    except Exception as e:
        print(f"   ❌ Error browsing posts: {e}")

    # Test 6: Search posts
    print("\n6️⃣  Searching posts...")
    try:
        search_dto = SearchPostsDTO(query="test", tags=["test"])
        results = container.search_posts_use_case.execute(search_dto)
        print(f"   ✅ Found {len(results)} matching posts")
    except Exception as e:
        print(f"   ❌ Error searching: {e}")

    # Test 7: List agents
    print("\n7️⃣  Listing agents...")
    try:
        agents = container.list_agents_use_case.execute()
        print(f"   ✅ Found {len(agents)} agents")
        for agent in agents:
            print(f"   👤 {agent.agent_name}: {agent.description[:50]}...")
    except Exception as e:
        print(f"   ❌ Error listing agents: {e}")

    print("\n" + "=" * 60)
    print("✨ All tests completed!")
    print("=" * 60)
    print(f"\n📁 Data stored in: {data_dir}")
    print("🔍 You can inspect the files directly:")
    print(f"   - Agents: {data_dir}/agents/")
    print(f"   - Posts: {data_dir}/posts/")
    print(f"   - Indexes: {data_dir}/index/")


if __name__ == "__main__":
    main()
